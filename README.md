# ASOS Shop Server

![fastapi-sqlalchemy-asyncpg](/static/fsap_1.jpg)

<a name="readme-top"></a>

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
        <li><a href="#features">Features</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#usage">Usage</a></li>
        <li><a href="#rainbow-logs-with-rich">Rainbow logs with rich</a></li>
      </ul>
    </li>
  </ol>
</details>

## About The Project

ASOS Shop Server is an API built to scrape discounted products from asos.com, focusing on famous brands like The North Face, New Balance, Levi's, and more. The server scrapes only discount products from these brands and saves them in a PostgreSQL database. The API provides endpoints to access the list of products based on category, subcategory, and brands.

### Built With

[![FastAPI][fastapi.tiangolo.com]][fastapi-url]
[![Pydantic][pydantic.com]][pydantic-url]
[![SQLAlchemy][sqlalchemy.org]][sqlalchemy-url]
[![Uvicorn][uvicorn.org]][uvicorn-url]
[![asyncpg][asyncpg.github.io]][asyncpg-url]
[![alembic][alembic.sqlalchemy.org]][alembic-url]
[![docker][hub.docker.com]][docker-url]
[![rich][rich.readthedocs.io]][rich-url]
[![redis][redis.io]][redis-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Features

- Scrapes discounted products from asos.com
- Filters products from famous brands like The North Face, New Balance, Levi's, etc.
- Saves scraped products in a PostgreSQL database
- Provides endpoints to retrieve products based on category, subcategory, brands and discount %
- Sends notifications via Telegram about the scraped products

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/asos-shop-server.git
```

2. Navigate into the project directory:

```bash
cd asos-shop-server
```

3. Create a .env file in the project root directory and add the necessary environment variables. Here's an example:

```plaintext
POSTGRES_DB=asos_db
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
BOT_TOKEN="BOT_TOKEN"
USER_ID="USER_ID"
SCHEDULE_TIME="SCHEDULE_TIME"
```

4. Build and run the project with Docker Compose:

```bash
docker-compose up --build -d
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Usage

Once the server is running, you can access the API endpoints to retrieve product data:

- List all products:

```bash
GET /products
```

- Filter products by category:

```bash
GET /products?category={category_name}
```

- Filter products by subcategory:

```bash
GET /products?subcategory={subcategory_name}
```

- Filter products by brand:

```bash
GET /products?brand={brand_name}
```

- Filter products by discount percentage:

```bash
GET /products?min_discount={min_discount}
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Rainbow logs with rich :rainbow:

To deliver better user(developer) experience when watching logs with tons of information
from few emitters (which are really needy on development stage) project is using [rich](https://github.com/Textualize/rich) library.
Event with [rich](https://github.com/Textualize/rich) superpowers reading logs is not easy.
Found [rich](https://github.com/Textualize/rich) really nice -
but it took time to learn how to integrate it as logger object properly and keep it as singleton.

![sample-logs-with-rich](/static/logz.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[fastapi.tiangolo.com]: https://img.shields.io/badge/FastAPI-0.104.1-009485?style=for-the-badge&logo=fastapi&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[pydantic.com]: https://img.shields.io/badge/Pydantic-2.6.4-e92063?style=for-the-badge&logo=pydantic&logoColor=white
[pydantic-url]: https://docs.pydantic.dev/latest/
[sqlalchemy.org]: https://img.shields.io/badge/SQLAlchemy-2.0.28-bb0000?color=bb0000&style=for-the-badge&logo=sqlalchemy&logoColor=white
[sqlalchemy-url]: https://docs.sqlalchemy.org/en/20/
[uvicorn.org]: https://img.shields.io/badge/Uvicorn-0.29.0-6BA81E?style=for-the-badge&logo=uvicorn&logoColor=white
[uvicorn-url]: https://www.uvicorn.org/
[asyncpg.github.io]: https://img.shields.io/badge/asyncpg-0.29.0-2e6fce?style=for-the-badge&logo=postgresql&logoColor=white
[asyncpg-url]: https://magicstack.github.io/asyncpg/current/
[alembic.sqlalchemy.org]: https://img.shields.io/badge/alembic-1.13.1-6BA81E?style=for-the-badge&logo=alembic&logoColor=white
[alembic-url]: https://alembic.sqlalchemy.org/en/latest/
[hub.docker.com]: https://img.shields.io/badge/docker-26.1.1-2094f3?style=for-the-badge&logo=docker&logoColor=white
[docker-url]: https://docs.docker.com/
[rich.readthedocs.io]: https://img.shields.io/badge/rich-13.7.1-009485?style=for-the-badge&logo=rich&logoColor=white
[rich-url]: https://rich.readthedocs.io/en/latest/
[redis.io]: https://img.shields.io/badge/redis-5.0.4-bb0000?style=for-the-badge&logo=redis&logoColor=white
[redis-url]: https://redis.io/docs/latest/
