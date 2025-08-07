# Google Reviews API

A Django REST API for fetching, storing, and serving Google Reviews data with automatic daily updates and statistics tracking.

## 🚀 Features

- **Google Reviews Scraping** - Automated fetching of Google Reviews from Google Maps API
- **Django REST Framework** - Modern API development with comprehensive documentation
- **Docker & Docker Compose** - Easy deployment and development environment
- **Swagger/OpenAPI Documentation** - Interactive API documentation with drf-spectacular
- **SQLite Database** - Lightweight and persistent data storage
- **Automatic Daily Updates** - Middleware-based daily review fetching
- **Statistics Tracking** - Daily review statistics and metrics
- **Admin Interface** - Django admin for data management

## 📋 Requirements

- Docker
- Docker Compose

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd google_reviews
   ```

2. **Build and run with Docker:**
   ```bash
   docker-compose up --build
   ```

3. **Run in background:**
   ```bash
   docker-compose up -d --build
   ```

4. **Stop containers:**
   ```bash
   docker-compose down
   ```

## 🌐 Access Points

- **Django Admin:** http://localhost:8000/admin
- **API Documentation (Swagger):** http://localhost:8000/api/docs/
- **API Documentation (ReDoc):** http://localhost:8000/api/redoc/
- **OpenAPI Schema:** http://localhost:8000/api/schema/
- **Google Reviews API:** http://localhost:8000/api/reviews/

## 📁 Project Structure

```
google_reviews/
├── src/
│   ├── apps/
│   │   └── google_reviews/          # Main Django app
│   │       ├── models.py            # Database models
│   │       ├── views.py             # API views
│   │       ├── serializers.py       # API serializers
│   │       ├── admin.py             # Admin interface
│   │       ├── urls.py              # URL routing
│   │       ├── middleware.py        # Daily update middleware
│   │       └── management/
│   │           └── commands/
│   │               ├── get_google_reviews.py           # Fetch reviews from Google
│   │               ├── update_google_review_stats.py   # Update statistics
│   │               └── daily_google_reviews_update.py  # Daily update orchestrator
│   └── core/                        # Django settings
│       ├── settings.py              # Project settings
│       └── urls.py                  # Main URL configuration
├── Dockerfile                       # Docker image configuration
├── docker-compose.yml              # Docker Compose services
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🗄️ Database Models

### GoogleReview
- **name** - Reviewer's name
- **href** - Review URL
- **avatar_url** - Reviewer's avatar image URL
- **text** - Review text content
- **rating** - Review rating (1-5 stars)
- **date** - Review date
- **profile_url** - Reviewer's Google profile URL
- **created_at** - Record creation timestamp

### GoogleReviewStatistics
- **date** - Statistics date
- **total_reviews** - Total number of reviews
- **total_rating** - Sum of all ratings
- **average_rating** - Average rating

### TaskExecution
- **task_name** - Name of the executed task
- **last_executed** - Last execution date

## 🔌 API Endpoints

### Google Reviews
- **GET** `/api/reviews/` - Get all Google reviews
  - Returns: List of review objects with name, rating, text, date, etc.

### Google Review Statistics
- **GET** `/api/reviews/statistics/` - Get review statistics (currently disabled)
  - Returns: Daily statistics including total reviews and average rating

## 🤖 Management Commands

### get_google_reviews
Fetches reviews from Google Maps API and stores them in the database:
```bash
docker-compose exec web python src/manage.py get_google_reviews
```

### update_google_review_stats
Updates or creates daily statistics:
```bash
docker-compose exec web python src/manage.py update_google_review_stats
```

### daily_google_reviews_update
Orchestrates daily updates (fetches reviews + updates stats):
```bash
docker-compose exec web python src/manage.py daily_google_reviews_update
```

## 🔄 Automatic Updates

The system includes automatic daily updates through:

1. **Middleware** - `DailyGoogleReviewsMiddleware` checks on each request if daily update is needed
2. **Task Tracking** - `TaskExecution` model prevents duplicate daily runs
3. **Logging** - Comprehensive logging of update operations

## 🛠️ Development

### Running Migrations
```bash
docker-compose exec web python src/manage.py migrate
```

### Creating Migrations
```bash
docker-compose exec web python src/manage.py makemigrations
```

### Creating Superuser
```bash
docker-compose exec web python src/manage.py createsuperuser
```

### Django Shell
```bash
docker-compose exec web python src/manage.py shell
```

### View Logs
```bash
docker-compose logs -f web
```

## 🔧 Environment Variables

Key environment variables in `docker-compose.yml`:
- `DEBUG=1` - Enable debug mode (set to 0 for production)

## 📚 API Documentation

The project uses **drf-spectacular** for automatic API documentation generation:

- **Swagger UI:** http://localhost:8000/api/docs/
- **ReDoc:** http://localhost:8000/api/redoc/

Features include:
- Interactive API testing
- Request/response examples
- Field descriptions and validation
- Choice field options

## 🐳 Docker Commands

### Rebuild without cache
```bash
docker-compose build --no-cache
```

### Remove all containers and volumes
```bash
docker-compose down -v
docker system prune -f
```

### View running containers
```bash
docker-compose ps
```

## 🔒 Security Notes

- Admin interface should be secured in production
- Consider using environment files for sensitive data
- Google Maps API URL is hardcoded (consider making it configurable)

## 🔗 How to Get Google Maps Reviews URL

The application uses a specific Google Maps API URL to fetch reviews. Here's how to obtain this URL:

### Method 1: Browser Developer Tools
1. **Go to Google Maps** and search for your business
2. **Open Developer Tools** (F12 or right-click → Inspect)
3. **Go to Network tab** and refresh the page
4. **Look for requests** containing `listugcposts` in the URL
5. **Copy the full URL** from the request

### Method 2: Manual URL Construction
The URL follows this pattern:
```
https://www.google.com/maps/rpc/listugcposts?authuser=0&hl=uk&gl=ua&pb=!1m6!1s[PLACE_ID]!6m4!4m1!1e1!4m1!1e3!2m2!1i10!2s!5m2!1s[REVIEW_ID]!7e81!8m9!2b1!3b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!11m0!13m1!1e1
```

Where:
- `[PLACE_ID]` - Your business Place ID (found in Google Maps URL)
- `[REVIEW_ID]` - Specific review identifier
- `hl=uk&gl=ua` - Language and country settings

### Method 3: Using Google Places API
1. **Get your Place ID** from Google Places API
2. **Use the Place ID** to construct the reviews URL
3. **Test the URL** in browser to ensure it returns reviews

### Current URL in Code
The current hardcoded URL in `get_google_reviews.py`:
```
https://www.google.com/maps/rpc/listugcposts?authuser=0&hl=uk&gl=ua&pb=!1m6!1s0x473a4d44bfebb121%3A0xc00b62ac9cc3b494!6m4!4m1!1e1!4m1!1e3!2m2!1i10!2s!5m2!1sZwGRaPT9CPK_wPAP1YfcwAo!7e81!8m9!2b1!3b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!11m0!13m1!1e1
```

### ⚠️ Important Notes
- **URLs may expire** and need periodic updates
- **Rate limiting** may apply to Google Maps API
- **Terms of Service** - Ensure compliance with Google's terms
- **Consider making URL configurable** via environment variables

## 🚀 Production Deployment

For production deployment:
1. Set `DEBUG=0` in environment
2. Use proper database (PostgreSQL recommended)
3. Configure proper logging
4. Set up SSL/TLS certificates
5. Use environment files for secrets
6. Consider rate limiting for Google Maps API calls

## 📝 License

This project is proprietary software.

## 👥 Contributing

For development:
1. Create feature branch
2. Make changes
3. Test with Docker
4. Submit pull request

## 🆘 Support

For technical support, contact the development team.