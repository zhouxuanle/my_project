CREATE  TABLE IF NOT EXISTS `users` (
  `id` varchar(255) PRIMARY KEY,
  `user_name` varchar(255),
  `real_name` varchar(255),
  `phone_number` varchar(255),
  `sex` varchar(255),
  `job` varchar(255),
  `company` varchar(255),
  `email` varchar(255),
  `password` varchar(255),
  `birth_of_date` date,
  `age` int,
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE  TABLE IF NOT EXISTS `addresses` (
  `id` varchar(255) PRIMARY KEY,
  `user_id` varchar(255),
  `title` varchar(255),
  `address_line` varchar(255),
  `country` varchar(255),
  `city` varchar(255),
  `postal_code` varchar(255),
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE  TABLE IF NOT EXISTS `categories` (
  `id` varchar(255) PRIMARY KEY,
  `name` varchar(255),
  `description` varchar(255),
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE  TABLE IF NOT EXISTS `sub_categories` (
  `id` varchar(255) PRIMARY KEY,
  `parent_id` varchar(255),
  `name` varchar(255),
  `description` varchar(255),
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE  TABLE IF NOT EXISTS `products` (
  `id` varchar(255) PRIMARY KEY,
  `name` varchar(255),
  `description` varchar(255),
  `category_id` varchar(255),
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE  TABLE IF NOT EXISTS `products_skus` (
  `id` varchar(255) PRIMARY KEY,
  `product_id` varchar(255),
  `price` varchar(255),
  `stock` integer,
  `created_at` timestamp,
  `deleted_at` timestamp
);

CREATE  TABLE IF NOT EXISTS `wishlist` (
  `id` varchar(255) PRIMARY KEY,
  `user_id` varchar(255),
  `products_sku_id` varchar(255),
  `created_at` timestamp,
  `deleted_at` timestamp
);


CREATE  TABLE IF NOT EXISTS `order_details` (
  `id` varchar(255) PRIMARY KEY,
  `user_id` varchar(255),
  `payment_id` varchar(255),
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE  TABLE IF NOT EXISTS `order_item` (
  `id` varchar(255) PRIMARY KEY,
  `order_id` varchar(255),
  `products_sku_id` varchar(255),
  `quantity` integer,
  `created_at` timestamp,
  `updated_at` timestamp
);

CREATE  TABLE IF NOT EXISTS `payment_details` (
  `id` varchar(255) PRIMARY KEY,
  `amount` integer,
  `provider` varchar(255),
  `status` varchar(255),
  `created_at` timestamp,
  `updated_at` timestamp
);

ALTER TABLE `addresses` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `wishlist` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `order_details` ADD FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

ALTER TABLE `wishlist` ADD FOREIGN KEY (`products_sku_id`) REFERENCES `products_skus` (`id`);

ALTER TABLE `order_item` ADD FOREIGN KEY (`products_sku_id`) REFERENCES `products_skus` (`id`);

ALTER TABLE `order_details` ADD FOREIGN KEY (`payment_id`) REFERENCES `payment_details` (`id`);

ALTER TABLE `order_item` ADD FOREIGN KEY (`order_id`) REFERENCES `order_details` (`id`);

ALTER TABLE `sub_categories` ADD FOREIGN KEY (`parent_id`) REFERENCES `categories` (`id`);

ALTER TABLE `products` ADD FOREIGN KEY (`category_id`) REFERENCES `sub_categories` (`id`);

ALTER TABLE `products_skus` ADD FOREIGN KEY (`product_id`) REFERENCES `products` (`id`);


