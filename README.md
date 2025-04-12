# 🕵️‍♂️ CacheMeIfYouCan

**A lightweight HTTP proxy downloader written in Python using raw sockets.**  
It fetches files on your behalf, handles errors, and deals with large content — all while keeping things fast and minimal.

---

## 🚀 Features

- Acts as a basic HTTP proxy server
- Downloads content from given URLs
- Handles large files using buffered reads
- Gracefully handles `404 Not Found` errors
- Built with only Python standard libraries
- Logs HTTP status codes and connection info
- Easy to run from the command line

---

## 📦 How It Works

The proxy listens on a custom port (e.g., `12345`) and waits for incoming requests from a browser like Firefox.

Once a request is received:
1. It extracts the host and file path.
2. Connects to the actual web server via sockets.
3. Sends an HTTP GET request.
4. Receives the response and writes the content to a file.
5. Continues listening for more requests.

---

## 🧠 Use Case

Originally developed as part of a **CS421 Computer Networks** programming assignment at Bilkent University.

---

## 🛠️ Requirements

- Python 3.x
- Works cross-platform (tested on Linux)

_No external libraries are needed._