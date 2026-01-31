# Google Workspace Bulk User Deletion Tool

A Python-based automation utility designed to streamline the process of offboarding large volumes of users from a Google Workspace domain using the Google Admin SDK Directory API.

## 📌 Project Overview
During my IT internship at Missions of Hope (MOHI) International, I was tasked with deleting **391 archived user accounts**. Manually searching and deleting each account via the Admin Console would have been inefficient and prone to human error. I developed this script to automate the process, reducing a multi-hour task to just a few minutes of execution time.

## 🚀 Features
- **Bulk Processing:** Reads user emails from a CSV export and processes deletions in a loop.
- **OAuth 2.0 Authentication:** Implements secure authorization via Google Cloud Console.
- **Error Handling:** Gracefully handles instances where users may have already been deleted or do not exist (HTTP 404 errors).
- **Virtual Environment Setup:** Ensures dependency isolation for a clean development workspace.

## 🛠️ Technologies Used
- **Language:** Python 3.x
- **APIs:** Google Admin SDK (Directory API)
- **Libraries:** `google-api-python-client`, `google-auth-oauthlib`
- **Tools:** VS Code, Git, Google Cloud Console

## 📋 Prerequisites
- A Google Workspace Admin account with privileges to delete users.
- A project created in the [Google Cloud Console](https://console.cloud.google.com/) with the **Admin SDK API** enabled.
- `credentials.json` file downloaded from the Cloud Console (OAuth 2.0 Client ID).



## 🔧 Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/yourusername/User-Management.git](https://github.com/yourusername/User-Management.git)
   cd User-Management