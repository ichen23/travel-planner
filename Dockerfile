FROM node:18-alpine AS frontend-build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM python:3.11-slim AS backend
WORKDIR /app

COPY --from=frontend-build /app/backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=frontend-build /app/backend ./backend
COPY --from=frontend-build /app/dist ./backend/dist

WORKDIR /app/backend

ENV PORT=8000

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
