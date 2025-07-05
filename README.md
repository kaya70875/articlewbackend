# 🧠 articlewbackend

The **backend service** for the [Articlew](https://github.com/kaya70875/articlew) platform — an educational app that generates intelligent, contextualized English sentences from real-world articles and content.

This backend is built with **FastAPI** and powers the sentence generation engine and APIs consumed by the frontend.

---

## 🎯 Overview

This service acts as the brain of the Articlew platform, handling:

- Sentence generation based on word input and article data
- Providing REST APIs for frontend communication
- AI tools like fix sentence, compare words and paraphrase.
- Fully integrated Paddle subscription system.

It works together with:
- [`articlewscraper`](https://github.com/kaya70875/articlewscraper): a microservice that crawls and saves articles to the database.
- [`articlew`](https://github.com/kaya70875/articlew): the frontend application that interacts with this backend.

---

## ⚙️ Features

- ✍️ **Word-based Sentence Generation**  
  Generates natural example sentences for a user-provided word across different article topics.

- 🧠 **Smart Filtering**  
  Filters sentences by topic, word inclusion, length, and article source.

- 🔐 **Authentication**  
  OAuth (e.g., Google) token-based authentication using FastAPI dependencies.

- 🧪 **API-First Design**  
  Fully RESTful and integrates easily with web or mobile frontends.

---

## 🛠️ Tech Stack

| Layer             | Technology         |
|------------------|--------------------|
| Language         | Python 3.11         |
| Framework        | FastAPI            |
| Database         | MongoDB Atlas      |
| Caching          | Redis              |
| Auth             | OAuth (Google) + JWT |
| Hosting          | Railway (Backend)  |
| Related Tools    | Pydantic, Uvicorn |
