# MonkeyStudyCo

#Postgres code
CREATE TABLE "user-actions"(
    "user_action_id" INTEGER NOT NULL,
    "task_id" INTEGER NOT NULL,
    "updated_progress" DOUBLE PRECISION NOT NULL,
    "datetime" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "user-actions" ADD PRIMARY KEY("user_action_id");
CREATE INDEX "user_actions_task_id_index" ON
    "user-actions"("task_id");
CREATE TABLE "certificates"(
    "id" bigserial NOT NULL,
    "telegram_id" INTEGER NOT NULL,
    "textbook_id" INTEGER NOT NULL,
    "image" JSON NOT NULL,
    "message_text" TEXT NOT NULL
);
ALTER TABLE
    "certificates" ADD PRIMARY KEY("id");
CREATE TABLE "textbook"(
    "textbook_id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "image" JSON NOT NULL
);
ALTER TABLE
    "textbook" ADD PRIMARY KEY("textbook_id");
CREATE TABLE "ai"(
    "ai_id" INTEGER NOT NULL,
    "Prompt" TEXT NOT NULL,
    "telegram_id" INTEGER NOT NULL
);
ALTER TABLE
    "ai" ADD PRIMARY KEY("ai_id");
CREATE TABLE "task"(
    "task_id" BIGINT NOT NULL,
    "textbook_id" INTEGER NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "task_text" TEXT NOT NULL,
    "task_solution" TEXT NOT NULL,
    "task_image" JSON NULL,
    "add_progress" DOUBLE PRECISION NULL,
    "is_done" BOOLEAN NOT NULL
);
ALTER TABLE
    "task" ADD PRIMARY KEY("task_id");
CREATE TABLE "tasks"(
    "id" SERIAL NOT NULL,
    "textbook_id" INTEGER NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "task_text" TEXT NOT NULL,
    "task_solution" TEXT NOT NULL,
    "task_image" JSON NULL,
    "add_progress" DOUBLE PRECISION NULL,
    "is_done" BOOLEAN NOT NULL
);
ALTER TABLE
    "tasks" ADD PRIMARY KEY("id");
CREATE TABLE "textbooks"(
    "id" SERIAL NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "image" JSON NOT NULL
);
ALTER TABLE
    "textbooks" ADD PRIMARY KEY("id");
CREATE TABLE "test"(
    "test_id" INTEGER NOT NULL,
    "textbook_id" INTEGER NOT NULL,
    "test_text" TEXT NOT NULL,
    "test_image" JSON NOT NULL
);
ALTER TABLE
    "test" ADD PRIMARY KEY("test_id");
CREATE TABLE "tests"(
    "id" SERIAL NOT NULL,
    "textbook_id" INTEGER NOT NULL,
    "test_text" TEXT NOT NULL,
    "test_image" JSON NOT NULL
);
ALTER TABLE
    "tests" ADD PRIMARY KEY("id");
CREATE TABLE "certificate"(
    "certificate_id" BIGINT NOT NULL,
    "telegram_id" INTEGER NOT NULL,
    "textbook_id" INTEGER NOT NULL,
    "image" JSON NOT NULL,
    "message_text" TEXT NOT NULL
);
ALTER TABLE
    "certificate" ADD PRIMARY KEY("telegram_id");
CREATE INDEX "certificate_textbook_id_index" ON
    "certificate"("textbook_id");
CREATE TABLE "users"(
    "id" SERIAL NOT NULL,
    "telegram_id" INTEGER NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "progress" DOUBLE PRECISION NOT NULL,
    "is_admin" BOOLEAN NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_telegram_id_unique" UNIQUE("telegram_id");
CREATE TABLE "notifications"(
    "telegram_id" INTEGER NOT NULL,
    "user_id" BIGINT NOT NULL,
    "text_message" VARCHAR(255) NOT NULL,
    "datetime" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "notifications" ADD PRIMARY KEY("telegram_id");
CREATE TABLE "Users"(
    "user_id" BIGINT NOT NULL,
    "telegram_id" INTEGER NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "updated_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "progress" DOUBLE PRECISION NOT NULL,
    "is_admin" BOOLEAN NOT NULL
);
ALTER TABLE
    "Users" ADD PRIMARY KEY("user_id");
ALTER TABLE
    "Users" ADD CONSTRAINT "users_telegram_id_unique" UNIQUE("telegram_id");
CREATE TABLE "admin_actions"(
    "telegram_id" INTEGER NOT NULL,
    "username" VARCHAR(255) NOT NULL,
    "updated_task_id" INTEGER NOT NULL,
    "updated_text" VARCHAR(255) NOT NULL,
    "updated_image" JSON NOT NULL,
    "updated_solution" VARCHAR(255) NOT NULL,
    "updated_progress" DOUBLE PRECISION NOT NULL,
    "datetime" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "admin_actions" ADD PRIMARY KEY("telegram_id");
CREATE INDEX "admin_actions_updated_task_id_index" ON
    "admin_actions"("updated_task_id");
CREATE TABLE "test_variant"(
    "test_variant_id" INTEGER NOT NULL,
    "variant_text" VARCHAR(255) NOT NULL,
    "iscorrect" BOOLEAN NOT NULL,
    "add_progress" BIGINT NOT NULL
);
ALTER TABLE
    "test_variant" ADD PRIMARY KEY("test_variant_id");
ALTER TABLE
    "Users" ADD CONSTRAINT "users_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "notifications"("telegram_id");
ALTER TABLE
    "test" ADD CONSTRAINT "test_textbook_id_foreign" FOREIGN KEY("textbook_id") REFERENCES "textbook"("textbook_id");
ALTER TABLE
    "ai" ADD CONSTRAINT "ai_telegram_id_foreign" FOREIGN KEY("telegram_id") REFERENCES "Users"("telegram_id");
ALTER TABLE
    "certificate" ADD CONSTRAINT "certificate_telegram_id_foreign" FOREIGN KEY("telegram_id") REFERENCES "Users"("telegram_id");
ALTER TABLE
    "user-actions" ADD CONSTRAINT "user_actions_task_id_foreign" FOREIGN KEY("task_id") REFERENCES "task"("task_id");
ALTER TABLE
    "certificate" ADD CONSTRAINT "certificate_textbook_id_foreign" FOREIGN KEY("textbook_id") REFERENCES "textbook"("textbook_id");
ALTER TABLE
    "certificates" ADD CONSTRAINT "certificates_telegram_id_foreign" FOREIGN KEY("telegram_id") REFERENCES "users"("telegram_id");
ALTER TABLE
    "Users" ADD CONSTRAINT "users_telegram_id_foreign" FOREIGN KEY("telegram_id") REFERENCES "admin_actions"("telegram_id");
ALTER TABLE
    "admin_actions" ADD CONSTRAINT "admin_actions_updated_task_id_foreign" FOREIGN KEY("updated_task_id") REFERENCES "task"("task_id");
ALTER TABLE
    "test_variant" ADD CONSTRAINT "test_variant_test_variant_id_foreign" FOREIGN KEY("test_variant_id") REFERENCES "test"("test_id");
ALTER TABLE
    "task" ADD CONSTRAINT "task_task_id_foreign" FOREIGN KEY("task_id") REFERENCES "textbook"("textbook_id");
ALTER TABLE
    "Users" ADD CONSTRAINT "users_telegram_id_foreign" FOREIGN KEY("telegram_id") REFERENCES "user-actions"("user_action_id");
ALTER TABLE
    "certificates" ADD CONSTRAINT "certificates_textbook_id_foreign" FOREIGN KEY("textbook_id") REFERENCES "textbooks"("id");
ALTER TABLE
    "tests" ADD CONSTRAINT "tests_textbook_id_foreign" FOREIGN KEY("textbook_id") REFERENCES "textbooks"("id");
ALTER TABLE
    "tasks" ADD CONSTRAINT "tasks_textbook_id_foreign" FOREIGN KEY("textbook_id") REFERENCES "textbooks"("id");
