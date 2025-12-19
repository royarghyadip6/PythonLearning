create database test;

create table users (
    id int primary key,
    name varchar(100) not null,
    email varchar(100) not null unique
);
insert into users (id, name, email) values (01,'Alice', 'alice@nokia.com');
insert into users (id, name, email) values (02,'Bob', 'bob@nokia.com');
insert into users (id, name, email) values (03,'Charlie', 'charlie@nokia.com');
select * from users;

SELECT * FROM test_vectors ORDER BY embedding <=> '[0.1, 0.02, 0.3]'::vector(3) LIMIT 5;