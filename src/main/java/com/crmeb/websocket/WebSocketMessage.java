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
public class WebSocketMessage {
    private String type;
    private String room;
    private String message;
}
