# SmartFlow Deployment Guide

## Quick Deploy to Railway.app

### Option 1: Railway.app (Recommended - Easiest)

1. **Create Railway Account**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub**
   - Push your code to GitHub repository
   - In Railway: Click "New Project" → "Deploy from GitHub"
   - Select your SmartFlow repository
   - Railway will auto-detect Python and use `Procfile`

3. **Wait for Build**
   - Railway will install dependencies from `requirements.txt`
   - Graph data (`graph_hcmc_full.gpickle`) is already included
   - Deploy takes ~3-5 minutes

4. **Get Your URL**
   - Railway provides a free URL like: `smartflow.up.railway.app`
   - Click "Open App" to access your website

**Cost**: FREE (Railway free tier: 500 hours/month)

---

### Option 2: Render.com

1. **Create Render Account**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Name**: smartflow
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120`

3. **Deploy**
   - Click "Create Web Service"
   - Wait ~5 minutes for deployment
   - Access via: `smartflow.onrender.com`

**Cost**: FREE (Render free tier with some limitations)

---

### Option 3: PythonAnywhere

1. **Create PythonAnywhere Account**
   - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Sign up for free account

2. **Upload Code**
   - Use "Files" tab to upload your project
   - Or clone from GitHub: `git clone https://github.com/yourusername/smartflow.git`

3. **Install Dependencies**
   - Open Bash console
   - Navigate to project: `cd smartflow`
   - Create virtualenv: `mkvirtualenv --python=/usr/bin/python3.11 smartflow`
   - Install: `pip install -r requirements.txt`

4. **Configure WSGI**
   - Go to "Web" tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.11
   - Edit WSGI file to point to your `app.py`

5. **Reload and Test**
   - Click "Reload" on Web tab
   - Access via: `yourusername.pythonanywhere.com`

**Cost**: FREE (1 web app limit on free tier)

---

## Production Checklist

✅ **Already Configured:**
- [x] `Procfile` created for Gunicorn
- [x] `gunicorn` added to `requirements.txt`
- [x] `runtime.txt` specifies Python 3.11
- [x] `app.py` uses environment variables (`PORT`, `DEBUG`)
- [x] Debug mode disabled by default (production-safe)
- [x] Graph data included in repository

⚠️ **Before Deploying:**
- [ ] Commit all changes to Git
- [ ] Ensure `graph_hcmc_full.gpickle` is committed (already tracked)
- [ ] Push to GitHub
- [ ] Choose deployment platform (Railway/Render/PythonAnywhere)

## Testing Deployment

After deployment, test these features:

1. **Homepage loads** - Check map displays correctly
2. **Find Route** - Select start/end points, verify route displays
3. **Mark Congestion** - Click points on map to mark congested roads
4. **Block Roads** - Verify routes avoid blocked segments
5. **Reset** - Test reset congestion button

## Environment Variables

Platforms automatically provide:
- `PORT` - Assigned by the platform
- `DEBUG` - Set to `False` by default (production mode)

No manual environment variables needed!

## Troubleshooting

### Deployment fails with timeout:
- Graph file is too large or OSM download takes too long
- **Solution**: Graph is already included in repo, so this shouldn't happen

### App crashes on startup:
- Check logs for missing dependencies
- Verify Python version matches `runtime.txt`

### Routes not working:
- Check if graph file loaded correctly
- View deployment logs for initialization messages

### Static files not loading:
- Verify `static/` and `templates/` folders are in repo
- Check file paths are relative, not absolute

## Custom Domain (Optional)

All platforms support custom domains:
- **Railway**: Settings → Domains → Add Custom Domain
- **Render**: Settings → Custom Domain → Add
- **PythonAnywhere**: Web tab → Add custom domain (paid plan only)

Configure DNS:
- Add CNAME record pointing to platform's domain
- Wait 24-48 hours for DNS propagation

## Scaling (If Needed)

Free tiers are sufficient for:
- Educational projects
- Demos
- Low traffic (<1000 requests/day)

For production traffic, upgrade to paid plans:
- **Railway**: $5/month for more resources
- **Render**: $7/month for always-on service
- **PythonAnywhere**: $5/month for custom domain + more resources

## Support

- Railway Docs: https://docs.railway.app
- Render Docs: https://render.com/docs
- PythonAnywhere Help: https://help.pythonanywhere.com

Good luck with deployment! 🚀
