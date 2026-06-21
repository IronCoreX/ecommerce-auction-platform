# Full-Stack E-Commerce Auction & Bidding Platform

A dynamic, multi-user e-commerce auction application built to handle real-time listings, bids, comments, and watchlist management. The system enforces strict relational database logic to manage auctions, process competitive bidding increments, and track closed listing winners.

## 📺 Live Video Demonstration

[![Watch the Auction Platform Demo](https://img.youtube.com/vi/bOoxmbPTb68/0.jpg)](https://youtu.be/bOoxmbPTb68)

*Click the image thumbnail above to watch the unlisted video walkthrough demonstrating live listing creation, bidding validation rules, relational comment feeds, and watchlist state management.*

## 🚀 Key Features Implemented
- **Active Auction Listings:** Allows authenticated users to create new marketplace listings by uploading an image URL, setting a starting bid price, selecting a category, and providing a description.
- **Dynamic Bidding Engine:** Enforces validation logic where any new bid must be strictly greater than the starting price and all previous bids. Updates the listing state immediately upon submission.
- **Closed Auctions & Winner Logistics:** Empowers listing creators to close an auction at any time, which permanently deactivates the listing and dynamically displays a "Winner" badge to the highest bidder.
- **Relational Watchlist System:** Features a toggle mechanism allowing users to save active listings to a personalized dashboard for centralized tracking.
- **Interactive Comment Timeline:** Implements a relational database relationship allowing authenticated users to post feedback and engage in open discussions on any listing page.
- **Categorized Index Filtering:** Includes a dedicated browsing panel that filters the active global database to display listings under specific marketplace categories.

## 🛠️ Technical Stack
- **Frontend Core:** HTML5, CSS3, Bootstrap (Responsive Grid Architecture)
- **Backend Architecture:** Python, Django (MTV Pattern)
- **Database Architecture:** SQLite (Relational models with Foreign Key constraints)
