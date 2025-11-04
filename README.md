# Nextmile(V1): Your AI-Powered Career Assistant 🚀

🌐 **Live Demo**: [https://nextmile.space](https://nextmile.space)  
> <span style="color:red;">(Currently unavailable — AWS billing issue, redeploying soon 🚀)</span>


🎥 **Video Demo:** [Watch on YouTube](https://www.youtube.com/watch?v=ikDGRWvs6Ag)

<p align="center">
  <a href="https://www.youtube.com/watch?v=ikDGRWvs6Ag" target="_blank">
    <img src="https://img.youtube.com/vi/ikDGRWvs6Ag/0.jpg" width="70%" alt="Nextmile Video Demo"/>
  </a>
</p>

Nextmile is an innovative open-source resume platform powered by AI. It provides a range of services for job seekers, including personal portfolio pages, interactive resume displays, and a digital twin (RAG) assistant to help them stand out from the crowd.

<center>
  <img src="Nextmile_logo.png" width="50%" alt="Nextmile logo"/>
</center>


✨ Key Features
Personal Portfolio Pages: Go beyond a static resume. Create a dynamic online presence that highlights your projects, skills, and unique personality.

Interactive Resume Displays: Make your application unforgettable. Present your experience in engaging, visually rich formats that captivate recruiters.

AI-powered Digital Twin (RAG) Assistant: Gain an unfair advantage. Our advanced AI assistant provides personalized feedback, helps you ace interviews, and offers tailored career advice.

Open-Source & Community-Driven: Join a transparent, continuously improving platform. Our open-source model ensures flexibility, customization, and a supportive community.

## 💻 Tech Stack  
Nextmile is built on a modern, robust foundation, ensuring a seamless and high-performance user experience.  

- **Frontend:** React, Next.js, Tailwind CSS  
- **Backend:** FastAPI (Python), Node.js  
- **Database:** MongoDB, ChromaDB  
- **AI/ML:** Python (LangChain, Huggingface Transformers, sentence-transformers)  
- **DevOps:** Docker, Docker Compose

## 🚀 Deployment

### Quick Deployment (Recommended)

Deploy to a new AWS EC2 server in one command:

```bash
git clone https://github.com/Ryanrc03/Nextmile.git
cd Nextmile
./scripts/deploy_to_new_server.sh --domain your-domain.com --email your-email@example.com
```

That's it! The script will automatically:
- ✅ Install all dependencies (Node.js, Python, Docker, Nginx, etc.)
- ✅ Configure environment variables
- ✅ Build the project
- ✅ Set up Nginx and SSL certificates
- ✅ Start all services
- ✅ Verify the deployment

### Migration from Old Server

Migrating from an existing server? Follow these steps:

1. **Backup old server** (run on old server):
   ```bash
   ./scripts/backup_before_migration.sh
   ```

2. **Deploy to new server**:
   ```bash
   ./scripts/deploy_to_new_server.sh --domain your-domain.com --email your-email@example.com
   ```

3. **Migrate data** (run on new server):
   ```bash
   ./scripts/migrate_data.sh --from old-server-ip --ssh-key ~/.ssh/key.pem
   ```

### Documentation

- 📖 [Deployment Scripts Guide](./DEPLOYMENT_SCRIPTS_GUIDE.md) - Detailed script usage
- 📖 [Migration Guide](./MIGRATION_GUIDE.md) - Complete manual deployment steps
- 📖 [Quick Reference](./DEPLOYMENT_QUICK_REFERENCE.txt) - Command cheat sheet
- 📖 [Documentation Index](./DEPLOYMENT_DOCS_INDEX.md) - Overview of all docs

### Available Scripts

| Script | Purpose |
|--------|---------|
| `deploy_to_new_server.sh` | One-click automated deployment |
| `init_new_server.sh` | Initialize server environment |
| `backup_before_migration.sh` | Backup data from old server |
| `migrate_data.sh` | Migrate data to new server |
| `check_deployment.sh` | Check deployment status |

All scripts are located in the `scripts/` directory.

