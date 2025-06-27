# 🧠 articlewbackend

The **backend service** for the [Articlew](https://github.com/kaya70875/articlew) platform — a powerful educational tool that generates intelligent, contextualized English sentences from real-world articles.

This backend is built with **FastAPI** and is responsible for handling sentence generation logic, managing crawl jobs and exposing APIs for the frontend.

---

## 🎯 Project Purpose

The goal of this backend is to serve as the **API and logic layer** of the Articlew system. It connects the frontend with crawled sentence data, generates content based on user input.

It works in conjunction with the [`articlewscraper`](https://github.com/kaya70875/articlewscraper) microservice that crawls articles and populates the database with sentence data.

---

## ⚙️ Features

- ✍️ **Sentence Generation**  
  Creates sample sentences based on user input (a word or phrase), filtered by topic, sentence length, and metadata.

- 🧩 **API Endpoints**  
  RESTful endpoints for user job status, sentence results, queue tracking, and more.

- 👤 **User Authentication**  
  Supports OAuth-based authentication (e.g., Google) and routes protected via FastAPI dependencies.

- 🔄 **Integration-Ready**  
  Designed to work seamlessly with the frontend (`articlew`) and the scraping microservice (`articlewscraper`).
