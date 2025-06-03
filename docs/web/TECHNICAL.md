# CompITA Web Interface Technical Guide

This document provides technical details about the CompITA Report Generator web interface architecture, components, and JavaScript implementation.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Frontend Structure](#frontend-structure)
3. [JavaScript Components](#javascript-components)
4. [CSS Styling System](#css-styling-system)
5. [API Integration](#api-integration)
6. [Browser Compatibility](#browser-compatibility)
7. [Performance Considerations](#performance-considerations)
8. [Development Guidelines](#development-guidelines)

## Architecture Overview

The CompITA Report Generator web interface is built using a modern web architecture:

- **Backend**: Flask web server with Jinja2 templates
- **Frontend**: HTML5, CSS3, and vanilla JavaScript
- **API Communication**: Fetch API for AJAX requests
- **Styling**: Custom CSS with responsive design

The web interface communicates with the CompITA API server, which is a separate FastAPI application. This separation allows for a clean architecture where:

1. The API server handles data processing, file operations, and report generation
2. The web interface provides a user-friendly way to interact with the API

## Frontend Structure

### Directory Structure

```
compita/src/web/
├── static/
│   ├── css/
│   │   └── styles.css
│   ├── js/
│   │   ├── app.js
│   │   ├── dashboard.js
│   │   ├── setup.js
│   │   └── flexible.js
│   └── images/
│       └── ...
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── generate.html
│   ├── upload.html
│   ├── reports.html
│   ├── flexible.html
│   └── setup.html
└── server.py
```

### Template Structure

The web interface uses a template inheritance pattern:

- `base.html`: The main template with common elements (header, footer, navigation)
- Page-specific templates that extend `base.html` and provide content for specific pages

Example template inheritance:

```html
{% extends "base.html" %}

{% block title %}CompITA Report Generator - Home{% endblock %}

{% block content %}
  <!-- Page-specific content here -->
{% endblock %}

{% block scripts %}
  <!-- Page-specific scripts here -->
{% endblock %}
```

## JavaScript Components

### Core Components

#### `app.js`

The main JavaScript file that initializes the application and provides core functionality:

- Global variables and configuration
- API URL management
- Page initialization based on current route
- Utility functions for date validation, file size formatting, etc.
- Task status polling mechanism
- Navigation handling

Key functions:
- `initDOMElements()`: Initializes DOM element references
- `fetchApiUrl()`: Fetches the API URL from the server
- `initCurrentPage()`: Initializes page-specific functionality
- `startStatusPolling()`: Polls for task status updates
- `updateTaskStatus()`: Updates the UI with task status information

#### `dashboard.js`

Handles the dashboard functionality on the home page:

- Recent projects display
- Recent reports display
- System status monitoring
- Auto-refresh mechanism
- Fallback data handling when API is unavailable

Key functions:
- `initDashboard()`: Initializes dashboard components
- `loadRecentProjects()`: Loads and displays recent projects
- `loadRecentReports()`: Loads and displays recent reports
- `checkSystemStatus()`: Checks API and storage status
- `storeCurrentPageDate()`: Stores date information in localStorage

#### `setup.js`

Manages project setup and validation functionality:

- Project creation form handling
- Project validation form handling
- Status display with loading indicators
- Validation error handling
- Directory structure display

Key functions:
- `showStatus()`: Displays status information with appropriate styling
- `showError()`: Displays error messages
- `pollTaskStatus()`: Polls for task status during project creation
- `showValidationError()`: Displays form validation errors
- `clearValidationErrors()`: Clears validation error messages

#### `flexible.js`

Handles the flexible reports generation:

- Module selection UI for flexible module reports
- Assessment type selection for flexible assessment reports
- Grade category and weight inputs for flexible grades reports
- Form submission and validation
- Dynamic UI updates based on user selections

### Common Patterns

1. **Event Listeners**: Added during DOM content loaded event
2. **Form Validation**: Client-side validation before API requests
3. **Status Updates**: Visual feedback during operations
4. **Error Handling**: User-friendly error messages
5. **Local Storage**: Caching data for improved performance

## CSS Styling System

The styling system uses a modular approach with:

- Base styles for typography, colors, and layout
- Component-specific styles for UI elements
- Utility classes for common patterns
- Responsive design using media queries

### Key CSS Components

- **Color Variables**: CSS variables for consistent color scheme
- **Grid System**: Flexible grid layouts for responsive design
- **Card Components**: Styled containers for content
- **Form Styles**: Consistent form element styling
- **Status Indicators**: Visual indicators for operation status
- **Loading Spinners**: Animated loading indicators
- **Responsive Breakpoints**: Media queries for different screen sizes

## API Integration

The web interface communicates with the API server using the Fetch API:

1. The API URL is fetched from the server on page load
2. API requests include proper headers and request bodies
3. Responses are handled with appropriate success and error flows
4. Background tasks are monitored through polling

### API URL Configuration

The API URL is configured in two ways:

1. Server-side: Set through environment variables
2. Client-side: Fetched from the server via the `/api_url` endpoint

This allows the web interface to work with different API server configurations without code changes.

## Browser Compatibility

The web interface is designed to work with modern browsers:

- Chrome 60+
- Firefox 60+
- Safari 12+
- Edge 79+

Key compatibility considerations:

- Using standard ES6 features with wide browser support
- Avoiding experimental CSS features
- Providing fallbacks for older browsers when necessary
- Testing across multiple browsers and devices

## Performance Considerations

Several techniques are used to ensure good performance:

1. **Minimal Dependencies**: No heavy JavaScript frameworks
2. **Efficient DOM Operations**: Minimizing reflows and repaints
3. **Lazy Loading**: Loading data only when needed
4. **Caching**: Using localStorage for non-critical data
5. **Throttling**: Limiting the frequency of API requests
6. **Optimized Assets**: Minimizing CSS and JavaScript

## Development Guidelines

When extending or modifying the web interface, follow these guidelines:

1. **Maintain Separation of Concerns**:
   - Keep HTML, CSS, and JavaScript separate
   - Use template inheritance for common elements
   - Organize JavaScript by functionality

2. **Follow Naming Conventions**:
   - Use descriptive, consistent naming
   - Prefix CSS classes to avoid conflicts
   - Use camelCase for JavaScript variables and functions

3. **Error Handling**:
   - Always handle API errors gracefully
   - Provide meaningful error messages to users
   - Include fallback mechanisms when possible

4. **Accessibility**:
   - Use semantic HTML elements
   - Include proper ARIA attributes
   - Ensure keyboard navigation works
   - Maintain sufficient color contrast

5. **Testing**:
   - Test across multiple browsers
   - Verify responsive design on different screen sizes
   - Test with network throttling to simulate slow connections
   - Validate HTML and CSS
