DELETE FROM categories;
DELETE FROM topics;
DELETE FROM posts;

INSERT INTO categories(cat_id, cat_name, cat_description) VALUES (1, 'Sloths', 'All things sloths.');
INSERT INTO categories(cat_id, cat_name, cat_description) VALUES (2, 'Cecropia', 'The best tree in existence.');
INSERT INTO categories(cat_id, cat_name, cat_description) VALUES (3, 'The Branch', 'Come and hang out!');

INSERT INTO topics(topic_id, topic_subject, topic_date, topic_cat, topic_by) VALUES (1, 'Ants!', NOW(), 1, 7);
INSERT INTO topics(topic_id, topic_subject, topic_date, topic_cat, topic_by) VALUES (2, 'Somebody call the bomb squad...', NOW(), 2, 8);
INSERT INTO topics(topic_id, topic_subject, topic_date, topic_cat, topic_by) VALUES (3, 'low key party at my branch', NOW(), 3, 9);

INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('Gonna have a chill party at my branch, probably eat some leaves... slowly. Maybe take a nap, and then hang for a bit. Reply if you\'re interested.', NOW(), 3, 7);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('I\'m down', NOW(), 3, 8);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('I\'ll bring leaves. Someone should get some caterpillars too. We\'ll make wraps.', NOW(), 3, 9);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('Solid. I\'m gonna take my second after-lunch nap, then lets do this. Head over whenever.', NOW(), 3, 10);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('Hey guys! Can I come?', NOW(), 3, 11);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('Darnit Steve, we just want to have a chill time without anyone crawling across our branches at mach 7.', NOW(), 3, 11);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('Aww give me a chance! Also I crashed my anteater into my branch. Can I borrow yours until mine gets fixed?', NOW(), 3, 9);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('This is why we can\'t have nice things steve.', NOW(), 3, 7);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('They\'re everywhere! Somebody help!!', NOW(), 1, 8);
INSERT INTO posts(post_content, post_date, post_topic, post_by) VALUES ('Because these leaves are exploding with flavor!', NOW(), 2, 9);
