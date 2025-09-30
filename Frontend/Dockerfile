# 多阶段构建 - 生产环境优化
FROM node:18-alpine AS base

# 安装 pnpm
RUN npm install -g pnpm

# 设置工作目录
WORKDIR /app

# 只复制依赖文件，利用Docker缓存
COPY package.json pnpm-lock.yaml ./

# 依赖安装阶段
FROM base AS deps
RUN pnpm install --frozen-lockfile

# 构建阶段
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# 创建 .env.local 的示例文件 (生产环境需要正确配置)
RUN echo "# Email Configuration" > .env.local && \
    echo "EMAIL_USER=your-email@gmail.com" >> .env.local && \
    echo "EMAIL_PASS=your-app-password" >> .env.local

# 构建应用
RUN pnpm build

# 生产运行阶段
FROM node:18-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

# 创建非root用户
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# 复制构建产物
COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

# 切换到非root用户
USER nextjs

# 暴露端口
EXPOSE 3000

ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

# 启动应用
CMD ["node", "server.js"]