using System;
using System.Collections.Generic;
using Bogus;

namespace MyProject.Backend.DataGeneration
{
    // POCO classes representing the generated entities
    public record UserInfo(string Id, string Username, string RealName, string PhoneNumber, string Sex, string Job, string Company, string Email, string Password, DateTime BirthOfDate, int Age, DateTime CreateTime, DateTime DeleteTime);

    public record Address(string Id, string UserId, string Title, string AddressLine, string Country, string City, string PostalCode, DateTime CreateTime, DateTime DeleteTime);

    public record Category(string Id, string Name, string Description, DateTime CreateTime, DateTime DeleteTime);

    public record Subcategory(string Id, string ParentId, string Name, string Description, DateTime CreateTime, DateTime DeleteTime);

    public record Product(string Id, string Name, string Description, string CategoryId, DateTime CreateTime, DateTime DeleteTime);

    public record Sku(string Id, string ProductId, decimal Price, long Quantity, DateTime CreateTime, DateTime DeleteTime);

    public record Wishlist(string Id, string UserId, string ProductsSkuId, DateTime CreateTime, DateTime DeleteTime);

    public record Cart(string Id, string OrderId, string ProductsSkuId, int Quantity, DateTime CreateTime, DateTime UpdatedAt);

    public record OrderDetails(string Id, string UserId, string PaymentId, DateTime CreateTime, DateTime UpdatedAt);

    public record OrderItem(string Id, string OrderId, string ProductsSkuId, long Quantity, DateTime CreateTime, DateTime UpdatedAt);

    public record PaymentDetails(string Id, decimal Amount, string Provider, string Status, DateTime CreateTime, DateTime UpdatedAt);


    // DataGenerator - uses Bogus to mimic logic from the Python generator
    // Usage:
    // 1. Create a .NET project (console/library) and add the Bogus NuGet package:
    //    dotnet add package Bogus
    // 2. Include this file in the project and call the DataGenerator methods.
    public class DataGenerator
    {
        private readonly Faker _faker;
        private readonly Random _random;

        public DataGenerator()
        {
            _faker = new Faker("en_US");
            _random = new Random();
        }

        public UserInfo GenerateUserData()
        {
            var createTime = DateTime.Now;
            // pick a delete_time between createTime and now (may equal createTime)
            var deleteTime = _faker.Date.Between(createTime, DateTime.Now);
            var birthOfDate = _faker.Date.PastOffset(_faker.Random.Int(18, 75) + 0, DateTime.Now).DateTime.Date;
            var age = DateTime.Now.Year - birthOfDate.Year;
            var userId = $"user_id-{Guid.NewGuid()}";
            var passwordDefault = _faker.Internet.Password();

            return new UserInfo(
                Id: userId,
                Username: _faker.Internet.UserName(),
                RealName: _faker.Name.FullName(),
                PhoneNumber: _faker.Phone.PhoneNumber(),
                Sex: _faker.PickRandom(new[] { "M", "F" , "Other" }),
                Job: _faker.Name.JobTitle(),
                Company: _faker.Company.CompanyName(),
                Email: _faker.Internet.Email(),
                Password: passwordDefault,
                BirthOfDate: birthOfDate,
                Age: age,
                CreateTime: createTime,
                DeleteTime: deleteTime
            );
        }

        public Address GenerateFakeAddress(UserInfo user)
        {
            var createTime = DateTime.Now;
            var deleteTime = _faker.Date.Between(createTime, DateTime.Now);
            var titles = new[] { "Home Address", "Work Address", "Billing Address", "Shipping Address", "Vacation Home" };
            var fullAddressLine = $"{_faker.Address.StreetAddress()} {_faker.Address.SecondaryAddress()}";
            var addressId = $"address_id-{Guid.NewGuid()}";

            return new Address(
                Id: addressId,
                UserId: user.Id,
                Title: _faker.PickRandom(titles),
                AddressLine: fullAddressLine,
                Country: _faker.Address.Country(),
                City: _faker.Address.City(),
                PostalCode: _faker.Address.ZipCode(),
                CreateTime: createTime,
                DeleteTime: deleteTime
            );
        }

        public Category GenerateCategoriesData()
        {
            var createTime = DateTime.Now;
            var deleteTime = _faker.Date.Between(createTime, DateTime.Now);
            var categoryId = $"category_id-{Guid.NewGuid()}";
            var categoryName = _faker.Commerce.Categories(1)[0];
            var description = _faker.Lorem.Sentence(10);

            return new Category(categoryId, categoryName, description, createTime, deleteTime);
        }

        public Subcategory GenerateSubcategoriesData(Category category)
        {
            var createTime = DateTime.Now;
            var deleteTime = _faker.Date.Between(createTime, DateTime.Now);
            var subcategoryId = $"subcategory_id-{Guid.NewGuid()}";
            // Replace .Capitalize() with char.ToUpper(word[0]) + word.Substring(1)
            var word = _faker.Lorem.Word();
            var subcategoryName = char.ToUpper(word[0]) + word.Substring(1) + " Subcategory";
            var description = _faker.Lorem.Sentence(8);

            return new Subcategory(subcategoryId, category.Id, subcategoryName, description, createTime, deleteTime);
        }

        public Product GenerateProductsData(Subcategory subcategory)
        {
            var createTime = DateTime.Now;
            var deleteTime = _faker.Date.Between(createTime, DateTime.Now);
            var productId = $"product_id-{Guid.NewGuid()}";
            var productName = _faker.Company.CatchPhrase();
            var productDescription = _faker.Lorem.Paragraph();

            return new Product(productId, productName, productDescription, subcategory.Id, createTime, deleteTime);
        }

        public Sku GenerateSkuData(Category category, Subcategory subcategory, Product product)
        {
            var createTime = DateTime.Now;
            var deleteTime = _faker.Date.Between(createTime, DateTime.Now);
            var skuNumber = _faker.Random.Number(10000, 99999);
            var skuId = $"{category.Id[^3..]}-{subcategory.Id[^3..]}-{product.Id[^3..]}-{skuNumber}";
            var price = Math.Round((decimal)(_faker.Random.Decimal(5.0m, 500.0m)), 2);
            var stock = _faker.Random.Long(0, 9_999_999);

            return new Sku(skuId, product.Id, price, stock, createTime, deleteTime);
        }

        public Wishlist GenerateWishlistData(Sku productsSku, UserInfo user)
        {
            var createTime = DateTime.Now;
            var deleteTime = _faker.Date.Between(createTime, DateTime.Now);
            var wishlistId = $"wishlist_id-{Guid.NewGuid()}";

            return new Wishlist(wishlistId, user.Id, productsSku.Id, createTime, deleteTime);
        }

        public Cart GenerateCartData(Sku productsSku, OrderDetails order)
        {
            var createTime = DateTime.Now;
            var updateTime = _faker.Date.Between(createTime, DateTime.Now);
            var cartId = $"cart_id-{Guid.NewGuid()}";
            var quantity = _faker.Random.Int(1, 9999);

            return new Cart(cartId, order.Id, productsSku.Id, quantity, createTime, updateTime);
        }

        public OrderDetails GenerateOrderDetailsData(UserInfo user, PaymentDetails payment)
        {
            var createTime = DateTime.Now;
            var updateTime = _faker.Date.Between(createTime, DateTime.Now);
            var orderDetailsId = $"order_details_id-{Guid.NewGuid()}";

            return new OrderDetails(orderDetailsId, user.Id, payment.Id, createTime, updateTime);
        }

        public OrderItem GenerateOrderItemData(Sku productsSku, OrderDetails order)
        {
            var createTime = DateTime.Now;
            var updateTime = _faker.Date.Between(createTime, DateTime.Now);
            var orderItemId = $"order_item_id-{Guid.NewGuid()}";
            var quantity = _faker.Random.Long(1, 99_999_999);

            return new OrderItem(orderItemId, order.Id, productsSku.Id, quantity, createTime, updateTime);
        }

        public PaymentDetails GeneratePaymentDetailsData()
        {
            var createTime = DateTime.Now;
            var updateTime = _faker.Date.Between(createTime, DateTime.Now);
            var paymentDetailsId = $"payment_details_id-{Guid.NewGuid()}";
            var paymentStatuses = new[] { "Success", "Pending", "Failed", "Refunded" };

            // provider: use credit card provider/brand as a short provider name
            var provider = _faker.Finance.CreditCardNumber();

            return new PaymentDetails(paymentDetailsId, 0m, provider, _faker.PickRandom(paymentStatuses), createTime, updateTime);
        }
    }
}
