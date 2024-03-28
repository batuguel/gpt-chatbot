import json

# Load sushi data
with open('sushi.json', 'r') as file:
    sushi_data = json.load(file)

# Prepare the context messages for the sushi data
def prepare_sushi_context():
    context_messages = [{"role": "system", "content": "You are a knowledgeable assistant that can provide information about sushi restaurants in a conversational way."}]
    for restaurant in sushi_data:
        # Basic information
        title = restaurant.get('title', 'A sushi restaurant')
        address = restaurant.get('address', 'an undisclosed location')
        lat = restaurant.get('position', {}).get('lat', 'unknown latitude')
        lng = restaurant.get('position', {}).get('lng', 'unknown longitude')
        distance = restaurant.get('distance_from_current_location', 'unknown')
        time_distance = restaurant.get('duration_from_current_location', 'unknown')
        categories = ', '.join(restaurant.get('categories', ['Various']))

        # Business hours - handling missing businessHours or formattedHours
        business_hours = restaurant.get('businessHours', {}).get('formattedHours', ['No business hours available'])
        if isinstance(business_hours, list):
            business_hours = ', '.join(business_hours)

        # Reviews
        average_rating = restaurant.get('reviews', {}).get('averageRating', 'no rating')
        review_count = restaurant.get('reviews', {}).get('reviewCount', 'no reviews')

        # Food types
        food_types = ', '.join(restaurant.get('foodTypes', ['Various']))

        # Price range
        price_range = restaurant.get('priceSummary', {}).get('priceRangeLevel', 'price range level is unavailable or undefined')

        # Constructing the context string
        context = (f"{title} is located at {address} at latitude {lat} and longitude {lng}. "
                   f"Distance to the current location is {distance}. The time it will take to get there is {time_distance}."
                   f"It belongs to the categories {categories} and business hours are {business_hours}. "
                   f"It has a rating of {average_rating} based on {review_count} reviews. "
                   f"Main food types include: {food_types} and the price range level is evaluated at {price_range}.")

        context_messages.append({"role": "system", "content": context})
    
    return context_messages