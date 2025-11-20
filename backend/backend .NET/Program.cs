using System;
using MyProject.Backend.DataGeneration;

// See https://aka.ms/new-console-template for more information
Console.WriteLine("Hello, World!");

var generator = new DataGenerator();

// Generate sample data
var user = generator.GenerateUserData();
var category = generator.GenerateCategoriesData();
var subcategory = generator.GenerateSubcategoriesData(category);
var product = generator.GenerateProductsData(subcategory);
var sku = generator.GenerateSkuData(category, subcategory, product);
var payment = generator.GeneratePaymentDetailsData();
var order = generator.GenerateOrderDetailsData(user, payment);

// Print generated data to console
Console.WriteLine("Generated User:");
Console.WriteLine(user);

Console.WriteLine("Generated Category:");
Console.WriteLine(category);

Console.WriteLine("Generated Product:");
Console.WriteLine(product);

Console.WriteLine("Generated SKU:");
Console.WriteLine(sku);

Console.WriteLine("Generated Payment:");
Console.WriteLine(payment);

Console.WriteLine("Generated Order:");
Console.WriteLine(order);
