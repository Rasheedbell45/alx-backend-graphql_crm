# Filter customers by name and creation date
   query {
     allCustomers(filter: { nameIcontains: "Ali", createdAtGte: "2025-01-01" }) {
       edges {
         node {
           id
           name
           email
           createdAt
         }
       }
     }
   }

   # Filter products by price range and sort by stock
   query {
     allProducts(filter: { priceGte: 100, priceLte: 1000 }, orderBy: "-stock") {
       edges {
         node {
           id
           name
           price
           stock
         }
       }
     }
   }

   # Filter orders by customer name, product name, and total amount
   query {
     allOrders(filter: { customerName: "Alice", productName: "Laptop", totalAmountGte: 500 }) {
       edges {
         node {
           id
           customer {
             name
           }
           product {
             name
           }
           totalAmount
           orderDate
         }
       }
     }
   }
