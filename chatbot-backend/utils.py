import json

# Load sushi data
with open('sushi.json', 'r') as file:
    sushi_data = json.load(file)

# Load parking data
with open('parking.json', 'r') as file:
    parking_data = json.load(file)

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


# Prepare the context messages for the parking data
def prepare_parking_context():
    context_messages = [{"role": "system", "content": "You are a knowledgeable assistant that can provide information about parking garages in a conversational way."}]
    for garage in parking_data:
        # Basic information
        title = garage.get('title', 'A parking garage')
        address = garage.get('address', 'an undisclosed location')
        lat = garage.get('position', {}).get('lat', 'unknown latitude')
        lng = garage.get('position', {}).get('lng', 'unknown longitude')
        distance = garage.get('distance_from_current_location', 'unknown')
        time_distance = garage.get('duration_from_current_location', 'unknown')
        categories = ', '.join(garage.get('categories', ['unknown']))

        # Business hours
        business_hours = garage.get('businessHours', {}).get('formattedHours', ['No business hours available'])
        if isinstance(business_hours, list):
            business_hours = ', '.join(business_hours)

        # Contact information
        phone_number = garage.get('contactInfo', {}).get('phoneNumber', 'no contact information')

        # Payment methods
        payment_methods = ', '.join(garage.get('paymentMethods', ['Various payment methods']))
        # Price summary
        price_summary = garage.get('priceSummary', {}).get('priceSummaryText', 'No price information available')
        # Including structured list prices
        list_prices = garage.get('priceStructured', {}).get('listPrices', [])
        price_details = ". ".join([f"{price['service']} service at rate: {price['price']}" for price in list_prices])

        # Parking details
        spots_number = garage.get('parking', {}).get('spotsNumber', 'unknown')
        free_spots_number = garage.get('parking', {}).get('freeSpotsNumber', 'unknown')
        disabled_spots_number = garage.get('parking', {}).get('disabledSpotsNumber', 'unknown')
        types = ', '.join(garage.get('parking', {}).get('types', []))
        services = ', '.join(garage.get('parking', {}).get('services', ['unknown']))

        #dimensions
        dimensions = garage.get('parking', {}).get('parkingDimensionRestriction', 'unknown')
        height = dimensions.get('height', 'unknown')
        width = dimensions.get('width', 'unknown')
        #operator
        operator = garage.get('parking', {}).get('operator', 'unknown operator')
        #availability
        availability = garage.get('parking', {}).get('availability', 'unknown')

        # Constructing the context string
        context = (f"{title} is located at {address} at latitude {lat} and longitude {lng}. "
                   f"Distance to the current location is {distance}, approximately a walk of {time_distance}."
                   f"It belongs to the categories {categories}. "
                   f"Business hours are {business_hours}. "
                   f"Contact info is: {phone_number}. "
                   f"Payment methods include: {payment_methods}. "
                   f"Price summary: {price_summary}. "
                   f"Structured price rates: {price_details}. "
                   f"This garage has {spots_number} spots in total, with {free_spots_number} spots currently available and {disabled_spots_number} spots for disabled parking. "
                   f"Services include: {services}. "
                   f"The garage has dimension restrictions of: height {height} and width {width}. "
                   f"Types of parking available are: {types}. "
                   f"The parking garage is operated by {operator}."
                   f"Current availability: {availability}.")

        context_messages.append({"role": "system", "content": context})
    
    return context_messages