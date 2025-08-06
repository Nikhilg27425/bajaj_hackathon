# Render Deployment Guide

## 🚀 Deploy to Render (No CLI Required)

### Step 1: Prepare Your Repository

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

### Step 2: Deploy on Render

1. **Go to [Render Dashboard](https://dashboard.render.com/)**
2. **Click "New +" → "Web Service"**
3. **Connect your GitHub repository**
4. **Configure the service:**

   **Basic Settings:**
   - **Name:** `document-qa-api` (or your preferred name)
   - **Environment:** `Python 3`
   - **Region:** Choose closest to you
   - **Branch:** `main`

   **Build & Deploy:**
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python3 app.py`

5. **Add Environment Variables:**
   - Click "Environment" tab
   - Add variable:
     - **Key:** `GROQ_API_KEY`
     - **Value:** Your Groq API key

6. **Click "Create Web Service"**

### Step 3: Get Your Webhook URL

Once deployed, Render will give you a URL like:
```
https://your-app-name.onrender.com
```

Your webhook URL will be:
```
https://your-app-name.onrender.com/hackrx/run
```

### Step 4: Test Your Webhook

```bash
curl -X POST "https://your-app-name.onrender.com/hackrx/run" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer 3eda6f3ac8aeaebd1954058607902b3759d6cbbf848dec41d470a19263cd7180" \
  -d '{
    "documents": "https://example.com/policy.pdf",
    "questions": ["What is the grace period for premium payment?"]
  }'
```

## ✅ Benefits of Render

- ✅ **Free tier available**
- ✅ **No CLI required**
- ✅ **Automatic HTTPS**
- ✅ **Custom domains**
- ✅ **Auto-deploy from GitHub**
- ✅ **Perfect for webhooks**

## 🔧 Troubleshooting

If you encounter issues:

1. **Check build logs** in Render dashboard
2. **Verify environment variables** are set correctly
3. **Ensure all dependencies** are in requirements.txt
4. **Check the health endpoint:** `https://your-app-name.onrender.com/` 