-- CreateTable
CREATE TABLE "nylas_account" (
    "id" TEXT NOT NULL,
    "grant_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,
    "user_id" TEXT NOT NULL,

    CONSTRAINT "nylas_account_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "email_message" (
    "id" TEXT NOT NULL,
    "starred" BOOLEAN NOT NULL,
    "unread" BOOLEAN NOT NULL,
    "folders" TEXT[],
    "date" INTEGER NOT NULL,
    "object" TEXT NOT NULL,
    "snippet" TEXT NOT NULL,
    "subject" TEXT NOT NULL,
    "thread_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL,
    "body" TEXT NOT NULL,
    "nylas_accountId" TEXT,

    CONSTRAINT "email_message_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "email_attachment" (
    "id" SERIAL NOT NULL,
    "filename" TEXT NOT NULL,
    "size" INTEGER NOT NULL,
    "content_type" TEXT NOT NULL,
    "is_inline" BOOLEAN,
    "content_disposition" TEXT,
    "message_id" TEXT NOT NULL,
    "nylas_account_id" TEXT,

    CONSTRAINT "email_attachment_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Sender" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "message_id" TEXT NOT NULL,

    CONSTRAINT "Sender_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "Recipient" (
    "id" SERIAL NOT NULL,
    "name" TEXT NOT NULL,
    "email" TEXT NOT NULL,
    "message_id" TEXT NOT NULL,

    CONSTRAINT "Recipient_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "nylas_account" ADD CONSTRAINT "nylas_account_user_id_fkey" FOREIGN KEY ("user_id") REFERENCES "user"("id") ON DELETE CASCADE ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "email_message" ADD CONSTRAINT "email_message_nylas_accountId_fkey" FOREIGN KEY ("nylas_accountId") REFERENCES "nylas_account"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "email_attachment" ADD CONSTRAINT "email_attachment_message_id_fkey" FOREIGN KEY ("message_id") REFERENCES "email_message"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "email_attachment" ADD CONSTRAINT "email_attachment_nylas_account_id_fkey" FOREIGN KEY ("nylas_account_id") REFERENCES "nylas_account"("id") ON DELETE SET NULL ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Sender" ADD CONSTRAINT "Sender_message_id_fkey" FOREIGN KEY ("message_id") REFERENCES "email_message"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Recipient" ADD CONSTRAINT "Recipient_message_id_fkey" FOREIGN KEY ("message_id") REFERENCES "email_message"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
