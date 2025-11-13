# News aggregator
**NewsAggregator** is a Django-based web application that aggregates news articles from various sources, 
allowing users to browse, search, translate and save articles for later reading.

---

##  Key Features

### For guest

- Browse, search, filter and translate news
- Choose system language (Ua/En)
- Sign Up, Log In

### For authorized user

- Browse, search, filter and translate news
- Choose system language (Ua/En)
- Save news articles to "Read later" list
- Edit profile credentials
- Log in

### For administrator

- Manage users and other data
- Monitor APIs status

---

##  Tech Stack

### Backend
- **Language**: Python 3.12
- **Framework**: Django 4.2
- **Database**: PostgreSQL 15
- **Testing:** Django test framework (unit, integration, E2E)

### Frontend
- **HTML5**
- **CSS3**
- **JavaScript**

---

##  Installation

**1. Clone the repository**
```bash
git clone https://github.com/dskarpets/news_aggregator
cd news_aggregator
```

**2. Create and activate virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate     # macOS/Linux
# or on Windows:
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Create a PostgreSQL database in pgAdmin**
1. Open pgAdmin
2. Right-click on Databases -> Create -> Database
3. Enter a name (for example, news_aggregator)
4. Click Save

**5. Configure database connection in Django**

In .env file update your username and password

**6. Make and apply migrations**

```
python manage.py makemigrations

python manage.py migrate
```

**7. (Optional) Create superuser**

```
python manage.py createsuperuser
```

**8. Run server**

```
python manage.py runserver
```
Then open http://127.0.0.1:8000/

---


## Author

**Student of IP-32 Daniil Karpets**

- Course work for a web application for news aggregator with automatic translation
- University: National Technical University of Ukraine "Igor Sikorsky Kyiv Polytechnic Institute"
