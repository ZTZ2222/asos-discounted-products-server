# ASOS Shop Server

![fastapi-sqlalchemy-asyncpg](/static/fsap_1.jpg)

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#make-will-help-you">Make will help you</a></li>
        <li><a href="#how-to-feed-database">How to feed database</a></li>
        <li><a href="#rainbow-logs-with-rich">Rainbow logs with rich</a></li>
        <li><a href="#setup-user-auth">Setup user auth</a></li>
        <li><a href="#local-development-with-poetry">Local development with poetry</a></li>
        <li><a href="#import-xlsx-files-with-polars-and-calamine">Import xlsx files with polars and calamine</a></li>
      </ul>
    </li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
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

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[fastapi.tiangolo.com]: https://img.shields.io/badge/FastAPI-0.104.1-009485?style=for-the-badge&logo=fastapi&logoColor=white
[fastapi-url]: https://fastapi.tiangolo.com/
[pydantic.com]: https://img.shields.io/badge/Pydantic-2.6.4-e92063?style=for-the-badge&logo=pydantic&logoColor=white
[pydantic-url]: https://docs.pydantic.dev/latest/
[sqlalchemy.org]: https://img.shields.io/badge/SQLAlchemy-2.0.28-bb0000?color=bb0000&style=for-the-badge
[sqlalchemy-url]: https://docs.sqlalchemy.org/en/20/
[uvicorn.org]: https://img.shields.io/badge/Uvicorn-0.29.0-2094f3?style=for-the-badge&logo=uvicorn&logoColor=white
[uvicorn-url]: https://www.uvicorn.org/
[asyncpg.github.io]: https://img.shields.io/badge/asyncpg-0.29.0-2e6fce?style=for-the-badge&logo=postgresql&logoColor=white
[asyncpg-url]: https://magicstack.github.io/asyncpg/current/
[alembic.sqlalchemy.org]: https://img.shields.io/badge/alembic-1.13.1-6BA81E?style=for-the-badge&logo=alembic&logoColor=white
[alembic-url]: https://alembic.sqlalchemy.org/en/latest/
