#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
  CREATE USER kratos;
  CREATE DATABASE kratos;
  \c kratos;
  GRANT USAGE ON SCHEMA public TO kratos;
  GRANT CREATE ON SCHEMA public TO kratos;
  ALTER USER kratos PASSWORD 'secret';
EOSQL
  
psql -v ON_ERROR_STOP=1 --username "postgres" <<-EOSQL
  CREATE USER api;
  CREATE DATABASE api;
  \c api;
  GRANT USAGE ON SCHEMA public TO api;
  GRANT CREATE ON SCHEMA public TO api;
  ALTER USER api PASSWORD 'secret';

  create table bots(
    bot_id serial primary key,
    img_path varchar(36) unique not null,
    name varchar(30) not null,
    gender varchar(15) not null,
    bio varchar(100) not null,
    character varchar(30)
  );

  create table bot_user(
    bot_user_id serial primary key,
    bot_id serial,
    foreign key (bot_id) references bots (bot_id),
    user_id char(36) not null
  );

  create table messages(
    message_id serial primary key,
    user_id char(36) not null,
    bot_id serial,
    foreign key (bot_id) references bots (bot_id),
    content text not null,
    from_bot bool default false
  );
EOSQL
