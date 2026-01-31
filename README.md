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
   ```

2. **Set up the Virtual Environment:**
   ```bash
   python -m venv venv

   # Windows
   .\venv\Scripts\activate

   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Add Credentials:**
   Place your `credentials.json` in the root directory.

## 📖 Usage

1. **Prepare your Data:**
   - Ensure your CSV file is in the root directory.
   - By default, the script looks for a column header named `Email Address [Required]`.
   - **Customization Tip:** If your CSV uses a different header (e.g., "User Email"), simply open `delete_users.py` and change the key in the following line to match your column name:
     ```python
     email = row['Your_Column_Name_Here']
     ```

2. **Run the Script:**
   ```bash
   python delete_users.py
   ```

3. **Authentication:**
   - A browser window will open automatically. Sign in with your authorized admin credentials.
   - If prompted with "Google hasn't verified this app," click **Advanced** -> **Go to [Project Name] (unsafe)** to grant permissions.

4. **Monitor Deletion:**
   - The terminal will output the status of each deletion in real-time.



## 🔒 Security Note
This repository utilizes a `.gitignore` file to ensure that sensitive files such as `credentials.json`, `token.json`, and private CSV data are never uploaded to version control.