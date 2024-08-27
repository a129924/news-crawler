# 使用官方的 PostgreSQL 镜像作为基础镜像
FROM postgres:latest

# 定义构建参数
ARG POSTGRES_USER
ARG POSTGRES_PASSWORD
ARG POSTGRES_DB

# 将构建参数转换为环境变量
ENV POSTGRES_USER=${POSTGRES_USER}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_DB=${POSTGRES_DB}

# 如果你有要初始化的 SQL 脚本或其他文件，可以将它们复制到容器中
COPY ./sql/create_company.sql /docker-entrypoint-initdb.d/

# 暴露 PostgreSQL 默认端口
EXPOSE 5432

# 设置默认启动命令（这一步通常由基础镜像完成）
CMD ["postgres"]

# 你可以在这里添加更多的自定义命令