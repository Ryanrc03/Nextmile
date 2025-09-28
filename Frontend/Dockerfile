# 使用 Node.js 官方镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package.json pnpm-lock.yaml ./

# 安装依赖
RUN npm install -g pnpm && pnpm install

# 复制应用代码
COPY . .

# 运行生产构建
RUN pnpm build

# 暴露应用端口
EXPOSE 3000

# 启动生产服务器
CMD ["pnpm", "start"]