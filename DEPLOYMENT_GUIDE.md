# CareerLens Deployment Guide - Railway + Vercel

Complete guide to deploy CareerLens with Railway (backend) and Vercel (frontend).

---

## 🚀 Part 1: Deploy Backend on Railway

### Step 1: Connect GitHub to Railway

1. Go to https://railway.app/
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose your `careerlens` repository
5. Click "Deploy"

### Step 2: Add Environment Variables

1. In Railway dashboard, go to your project
2. Click on the service
3. Go to "Variables" tab
4. Add:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
5. Click "Deploy" to redeploy with the new variable

### Step 3: Get Your Backend URL

1. In Railway dashboard, go to "Settings"
2. Find "Public URL" or "Domain"
3. Copy the URL (looks like: `https://careerlens-prod.up.railway.app`)
4. Save this - you'll need it for the frontend!

**Backend is now live!** ✅

---

## 🚀 Part 2: Deploy Frontend on Vercel

### Step 1: Update Frontend Configuration

Before deploying, update your frontend to use the Railway backend URL.

**Edit `careerlens-frontend/src/App.jsx`:**

Find this line:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

Replace with:
```javascript
const API_BASE_URL = 'https://your-railway-url.up.railway.app';
```

(Replace `your-railway-url` with your actual Railway URL from Step 3 above)

### Step 2: Push to GitHub

```bash
cd careerlens
git add .
git commit -m "Update API URL for production deployment"
git push origin main
```

### Step 3: Deploy on Vercel

1. Go to https://vercel.com/
2. Click "New Project"
3. Select your `careerlens` repository
4. Click "Import"
5. In "Root Directory", select `careerlens-frontend`
6. Click "Deploy"

### Step 4: Get Your Frontend URL

1. After deployment completes, you'll get a URL like:
   ```
   https://careerlens.vercel.app
   ```
2. This is your public shareable link!

**Frontend is now live!** ✅

---

## ✅ Verification

1. Go to your Vercel URL: `https://careerlens.vercel.app`
2. Upload a resume
3. Paste a job description
4. Click "Analyze"
5. You should see the AI analysis!

---

## 🔗 Share with Friends

Your public URL: `https://careerlens.vercel.app`

Share this link with your friends! They can use it without any setup.

---

## 🐛 Troubleshooting

### "Cannot connect to backend"
- Check that your Railway URL is correct in `App.jsx`
- Make sure GEMINI_API_KEY is set in Railway environment variables
- Redeploy both services

### "API Key error"
- Verify your Gemini API key is correct
- Go to https://ai.google.dev/ and check your key
- Update it in Railway Variables

### "CORS error"
- This is already configured in `main.py`
- If you still see it, check that Railway backend is running

---

## 📝 Environment Variables

### Railway (Backend)
```
GEMINI_API_KEY=your_google_gemini_api_key
```

### Vercel (Frontend)
No secrets needed - it just calls the Railway backend

---

## 🎉 You're Done!

Your CareerLens is now live and shareable! 🚀

**Share the link:** `https://careerlens.vercel.app`

---

## 📚 Additional Resources

- Railway Docs: https://docs.railway.app/
- Vercel Docs: https://vercel.com/docs
- Google Gemini API: https://ai.google.dev/

