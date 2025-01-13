package com.crmeb.websocket;

import lombok.Data;

/**
 * WebSocket Message
 * Represents a message in the WebSocket communication
 *
 * @author Devin
 * @since 2024-01-xx
 */
@Data
public class WebSocketMessage<T> {
    private String type;
    private String room;
    private String message;
    private T data;
    
    public static <T> WebSocketMessage<T> of(String type, String room, String message, T data) {
        WebSocketMessage<T> msg = new WebSocketMessage<>();
        msg.setType(type);
        msg.setRoom(room);
        msg.setMessage(message);
        msg.setData(data);
        return msg;
    }
}
