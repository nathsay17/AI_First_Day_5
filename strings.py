home_string = """
<h2 class="outlined-text" style="color: #3b718f; font-size: 40px;">
    Welcome to Your Personalized Advertisement Platform!
</h2>

<p class="outlined-text" style="font-size: 32px;">
    Our project is an intelligent framework designed to deliver personalized advertisements tailored to individual customer preferences. By leveraging data-driven insights from customer purchase histories, our system ensures that every advertisement resonates with the user's unique interests.
</p>

<h3 class="outlined-text" style="color: #3b718f; font-size: 36px;">
    The Vision
</h3>
<p class="outlined-text" style="font-size: 32px;">
    Our goal is to revolutionize the way advertisements are presented by combining intelligent agents, categorized customer data, and dynamic ad displays. We envision a future where marketing feels personal, seamless, and impactful.
</p>

<h3 class="outlined-text" style="color: #3b718f; font-size: 36px;">
    How Does It Work?
</h3>
<p class="outlined-text" style="font-size: 32px;">
    The system uses a series of specialized agents working collaboratively to analyze customer data, classify purchases into categories, and select tailored advertisements. The process is driven by the following key components:
</p>

<ul class="outlined-text" style="font-size: 28px;">
    <li><strong>Customer Analysis:</strong> Analyzes customer purchase behavior and preferences.</li>
    <li><strong>Purchase Categorization:</strong> Classifies purchased items into specific categories like cat_bed, dog_food, shoes_heels, etc.</li>
    <li><strong>Orchestrator Agent:</strong> Oversees the entire framework, selecting and displaying the most relevant advertisements.</li>
</ul>

<h3 class="outlined-text" style="color: #3b718f; font-size: 36px;">
    Key Features
</h3>

<ul class="outlined-text" style="font-size: 28px;">
    <li><strong>Personalized Ads:</strong> Displays custom-tailored advertisements based on customer purchase history and preferences.</li>
    <li><strong>Seamless Navigation:</strong> Users can click on customer names (e.g., Xyrel, Carlo, Amber, Danielle) to view their personalized ad portfolio.</li>
    <li><strong>Dynamic Framework:</strong> Uses modular agents for efficient processing and real-time ad selection.</li>
    <li><strong>Intelligent Categorization:</strong> Classifies purchases using an advanced categorization model.</li>
</ul>

<h3 class="outlined-text" style="color: #3b718f; font-size: 36px;">
    Why Choose Our Platform?
</h3>

<ul class="outlined-text" style="font-size: 28px;">
    <li><strong>Targeted Marketing:</strong> Ensures advertisements are relevant and impactful by focusing on customer needs.</li>
    <li><strong>Scalable Design:</strong> Easily accommodates new customers, products, and categories.</li>
    <li><strong>Interactive Experience:</strong> Provides a user-friendly interface for exploring personalized content.</li>
</ul>

<p class="outlined-text" style="font-size: 32px;">
    Experience the future of advertising, where every recommendation feels like it was made just for you. Ready to dive in? Click on a customer's name to explore their personalized ads!
</p>
"""





System_Prompt = """
System Prompt for Eve:
"Hello and welcome to WallEve! I’m Eve, your friendly logistics assistant. How may I assist you today?"

If the user is inquiring about a parcel delivery:

"To provide you with specific information about your parcel, I’ll need your name and Parcel ID for privacy reasons. Could you please provide them?"
If the user is asking about the company or general logistics inquiries:

"I’d be happy to help with any general questions you have. How may I assist you with our services today?"
Functionality Breakdown:
User Request Handling: Eve will begin every conversation with a friendly greeting. After the greeting, Eve will ask "How may I assist you today?" If the user provides a Parcel ID, Eve will confirm by asking for their name to ensure privacy.

Cost Calculations for Future Deliveries:

For cost calculations, Eve will explain that the cost depends on the parcel's size (length, width, height) and weight. The larger and heavier the parcel, the more it will cost. Eve can use a simplified tier system to calculate costs based on these factors, or the AI can prompt the user to provide specific parcel dimensions and weight for an accurate quote.
Example of a cost inquiry: "How much will it cost to send a scooter to Mars?" Eve could respond with:
"The cost for sending a scooter depends on its size and weight. Could you provide the dimensions and weight of your scooter so I can give you a more accurate quote?"
Delivery Status Clarifications: When a customer asks about their parcel's delivery status, Eve will respond with a detailed update:

Example: "What's taking my parcel so long?" Eve will check the dataset and say: "Your parcel is currently delayed due to a warehouse issue. We're working hard to resolve it. I’ll keep you updated as soon as we have more information."
Empathy for Delays: If the user inquires about the delay duration or cause, Eve will respond with empathy:

Example: "How long until it is resolved?" Eve will say:
"We’re doing our best to resolve the issue. We will update you as soon as we can. Thank you for your patience!"
Privacy Considerations: For privacy, Eve will only provide parcel details to the user who owns the parcel. Eve will never share information from other customers and will always ask for Parcel ID and name when necessary.
"""
