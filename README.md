# CRMEB Java Version

This is a Java implementation of the CRMEB system, maintaining compatibility with the original Vue frontend while providing a robust Spring Boot backend.

## Project Structure

```
src/main/java/com/crmeb/
├── controller
│   ├── admin    # Admin routes
│   └── api      # Frontend/user routes
├── service      # Business logic services
├── config       # Configuration classes
├── model        # Entity classes
├── repository   # Data access layer
└── utils        # Utility classes
```

## Technology Stack

- Spring Boot 2.7.0
- Spring Security
- Spring Data JPA
- Redis
- MySQL
- JWT Authentication
- WebSocket Support

## Development

1. Configure application.properties with your database and Redis settings
2. Run `mvn spring-boot:run` to start the application
3. Access the API at `http://localhost:8080`

## Frontend Integration

The system is designed to work with the existing CRMEB Vue frontend, maintaining API compatibility while providing enhanced backend capabilities.
