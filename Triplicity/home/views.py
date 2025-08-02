from django.shortcuts import render

# Create your views here.
def homepage(request):
    """Homepage with travel packages and hotels"""
    
    # Sample travel packages data
    travel_packages = [
        {
            "name": "Goa Beach Paradise",
            "location": "Goa, India",
            "price": "₹25,999",
            "duration": "4 Days / 3 Nights",
            "rating": 4.8,
            "features": ["Beach Resort", "Water Sports", "Local Cuisine", "Nightlife"],
            "image": "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?w=400"
        },
        {
            "name": "Kerala Backwaters",
            "location": "Kerala, India", 
            "price": "₹32,999",
            "duration": "6 Days / 5 Nights",
            "rating": 4.9,
            "features": ["Houseboat Stay", "Ayurveda Spa", "Tea Gardens", "Wildlife"],
            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
        },
        {
            "name": "Shimla Hill Station",
            "location": "Himachal Pradesh, India",
            "price": "₹28,999", 
            "duration": "5 Days / 4 Nights",
            "rating": 4.7,
            "features": ["Mountain Views", "Colonial Architecture", "Adventure Sports", "Cool Climate"],
            "image": "https://images.unsplash.com/photo-1586500036634-57495d9bf10e?w=400"
        },
        {
            "name": "Rajasthan Royal Heritage",
            "location": "Rajasthan, India",
            "price": "₹45,999",
            "duration": "8 Days / 7 Nights", 
            "rating": 4.8,
            "features": ["Palace Hotels", "Camel Safari", "Desert Camping", "Cultural Shows"],
            "image": "https://images.unsplash.com/photo-1477587458883-47145ed94245?w=400"
        },
        {
            "name": "Ladakh Adventure",
            "location": "Ladakh, India",
            "price": "₹55,999",
            "duration": "9 Days / 8 Nights",
            "rating": 4.9,
            "features": ["High Altitude", "Buddhist Monasteries", "Trekking", "Scenic Lakes"],
            "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400"
        },
        {
            "name": "Andaman Island Escape",
            "location": "Andaman & Nicobar",
            "price": "₹38,999",
            "duration": "6 Days / 5 Nights",
            "rating": 4.6,
            "features": ["Pristine Beaches", "Scuba Diving", "Island Hopping", "Water Villa"],
            "image": "https://images.unsplash.com/photo-1559827260-dc66d52bef19?w=400"
        }
    ]
    
    # Sample hotels data
    hotels_data = [
        {
            "name": "Luxury Beach Resort Goa",
            "location": "Candolim, Goa",
            "price": "₹8,999",
            "rating": 4.7,
            "amenities": ["Private Beach", "Spa", "Pool", "Restaurant"],
            "image": "https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=400"
        },
        {
            "name": "Heritage Palace Hotel",
            "location": "Udaipur, Rajasthan", 
            "price": "₹15,999",
            "rating": 4.9,
            "amenities": ["Lake View", "Heritage Property", "Fine Dining", "Cultural Program"],
            "image": "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400"
        },
        {
            "name": "Mountain View Resort",
            "location": "Manali, Himachal Pradesh",
            "price": "₹6,999",
            "rating": 4.5,
            "amenities": ["Mountain View", "Adventure Activities", "Bonfire", "Local Cuisine"],
            "image": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=400"
        },
        {
            "name": "Backwater Villa",
            "location": "Alleppey, Kerala",
            "price": "₹12,999",
            "rating": 4.8,
            "amenities": ["Backwater View", "Houseboat", "Ayurveda Spa", "Traditional Meals"],
            "image": "https://images.unsplash.com/photo-1520637836862-4d197d17c798?w=400"
        }
    ]
    
    # Sample user reviews
    user_reviews = [
        {
            "name": "Priya Sharma",
            "location": "Mumbai",
            "rating": 5,
            "review": "Amazing experience with Triplicity! The Goa package was perfectly planned. The hotel was fantastic and the beach activities were incredible. Highly recommended!",
            "package": "Goa Beach Paradise",
            "date": "March 2025"
        },
        {
            "name": "Rahul Patel", 
            "location": "Delhi",
            "rating": 5,
            "review": "Kerala backwaters trip was a dream come true. The houseboat experience was magical and the Ayurveda spa was so relaxing. Will definitely book again!",
            "package": "Kerala Backwaters",
            "date": "February 2025"
        },
        {
            "name": "Anita Desai",
            "location": "Bangalore",
            "rating": 4,
            "review": "Shimla trip was wonderful! The hill station was beautiful and the hotel had amazing mountain views. The only issue was the weather, but that's natural!",
            "package": "Shimla Hill Station", 
            "date": "January 2025"
        },
        {
            "name": "Vikram Singh",
            "location": "Pune",
            "rating": 5,
            "review": "Rajasthan heritage tour exceeded all expectations. The palace hotels were royal and the desert safari was thrilling. Exceptional service from Triplicity!",
            "package": "Rajasthan Royal Heritage",
            "date": "December 2024"
        }
    ]
    
    context = {
        'travel_packages': travel_packages,
        'hotels_data': hotels_data,
        'user_reviews': user_reviews,
    }
    
    return render(request, 'home/homepage.html', context)