import app from './app-test';

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`🚀 Server is running on port ${PORT}`);
  console.log(`📊 Health check: http://localhost:${PORT}/api/health`);
  console.log(`💼 Experience API: http://localhost:${PORT}/api/experience`);
  console.log(`🎯 Projects API: http://localhost:${PORT}/api/projects`);
});
