package com.crmeb.websocket;

import com.alibaba.fastjson.JSON;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.*;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.io.IOException;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

/**
 * WebSocket Handler
 * Replaces original Swoole WebSocket functionality
 * Handles real-time communication
 *
 * Features:
 * - Client connection management
 * - Room-based messaging
 * - Ping/Pong heartbeat
 * 
 * @author Devin
 * @since 2024-01-xx
 */
@Slf4j
@Component
@RequiredArgsConstructor
public class WebSocketHandler extends TextWebSocketHandler {

    private static final Map<String, WebSocketSession> clients = new ConcurrentHashMap<>();
    private static final Map<String, String> clientRooms = new ConcurrentHashMap<>();
    
    @Override
    public void afterConnectionEstablished(WebSocketSession session) {
        String sessionId = session.getId();
        clients.put(sessionId, session);
        log.info("Client connected: {}", sessionId);
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) {
        try {
            String payload = message.getPayload();
            WebSocketMessage<?> msg = JSON.parseObject(payload, WebSocketMessage.class);
            
            switch (msg.getType()) {
                case "join":
                    handleJoinRoom(session, msg.getRoom());
                    break;
                case "leave":
                    handleLeaveRoom(session);
                    break;
                case "message":
                    handleRoomMessage(msg.getRoom(), msg.getMessage());
                    break;
                case "ping":
                    session.sendMessage(new TextMessage("{\"type\":\"pong\"}"));
                    break;
            }
        } catch (Exception e) {
            log.error("Error handling message", e);
        }
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) {
        String sessionId = session.getId();
        handleLeaveRoom(session);
        clients.remove(sessionId);
        log.info("Client disconnected: {}", sessionId);
    }

    private void handleJoinRoom(WebSocketSession session, String room) {
        String sessionId = session.getId();
        clientRooms.put(sessionId, room);
        log.info("Client {} joined room {}", sessionId, room);
    }

    private void handleLeaveRoom(WebSocketSession session) {
        String sessionId = session.getId();
        clientRooms.remove(sessionId);
        log.info("Client {} left room", sessionId);
    }

    private void handleRoomMessage(String room, String message) {
        clientRooms.forEach((sessionId, clientRoom) -> {
            if (clientRoom.equals(room)) {
                WebSocketSession session = clients.get(sessionId);
                if (session != null && session.isOpen()) {
                    try {
                        session.sendMessage(new TextMessage(message));
                    } catch (IOException e) {
                        log.error("Error sending message to client {}", sessionId, e);
                    }
                }
            }
        });
    }
}
