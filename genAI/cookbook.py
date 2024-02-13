"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""
import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyARVdklzaC3HdyIbGTK8zonIMcy-vZ51pw")

# Set up the model
generation_config = {
  "temperature": 0.8,
  "top_p": 1,
  "top_k": 1,
  "max_output_tokens": 2048,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-pro",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": ["Suggest a recipe for a quick and healthy breakfast."]
  },
  {
    "role": "model",
    "parts": ["**Scrambled Eggs with Spinach and Tomatoes**\n\n**Ingredients:**\n\n- 2 large eggs\n- 1 tablespoon milk\n- Salt and pepper to taste\n- 1 tablespoon olive oil\n- 1/2 cup baby spinach\n- 1/2 cup chopped tomatoes\n- 1/4 cup crumbled feta cheese (optional)\n\n**Instructions:**\n\n1. In a small bowl, whisk together the eggs, milk, salt, and pepper.\n2. Heat the olive oil in a nonstick skillet over medium heat.\n3. Pour the egg mixture into the skillet and cook, stirring constantly, until the eggs are cooked through, about 2-3 minutes.\n4. Add the spinach and tomatoes to the skillet and cook, stirring occasionally, until the spinach is wilted and the tomatoes are heated through, about 1 minute.\n5. Season with additional salt and pepper to taste.\n6. Transfer the scrambled eggs to a plate and top with feta cheese, if desired.\n7. Serve immediately.\n\n**Tips:**\n- For a more protein-packed breakfast, add some cooked bacon, sausage, or ham to the scrambled eggs.\n- If you don't have baby spinach, you can use regular spinach, just be sure to chop it finely.\n- You can also add other vegetables to the scrambled eggs, such as diced bell peppers, mushrooms, or onions.\n- If you don't have feta cheese, you can use grated Parmesan cheese or shredded cheddar cheese instead."]
  },
  {
    "role": "user",
    "parts": ["Tell me a unique dessert recipe that includes carob"]
  },
  {
    "role": "model",
    "parts": ["**Carob Fudge Truffles**\n\n**Ingredients:**\n\n- 1 cup carob powder\n- 1/2 cup coconut oil, melted\n- 1/4 cup honey\n- 1/4 cup peanut butter\n- 1 tablespoon vanilla extract\n- 1/2 teaspoon sea salt\n- 1/4 cup chopped nuts, optional\n- 1/4 cup unsweetened cocoa powder, for coating\n\n**Instructions:**\n\n1. In a medium bowl, whisk together the carob powder, coconut oil, honey, peanut butter, vanilla extract, and sea salt until smooth and well combined.\n2. If the mixture is too thick to roll into balls, add a little more coconut oil or honey.\n3. If the mixture is too thin, add a little more carob powder.\n4. Stir in the chopped nuts, if desired.\n5. Line a baking sheet with parchment paper.\n6. Use a small spoon or your hands to roll the mixture into 1-inch balls.\n7. Place the balls on the prepared baking sheet.\n8. Freeze the truffles for at least 30 minutes, or until firm.\n9. In a shallow bowl, place the unsweetened cocoa powder.\n10. Roll each truffle in the cocoa powder to coat.\n11. Place the truffles in a single layer in an airtight container and store in the refrigerator for up to 2 weeks.\n\n**Tips:**\n\n- For a richer flavor, use dark chocolate carob powder.\n- You can also use almond butter or cashew butter instead of peanut butter.\n- If you don't have chopped nuts, you can use shredded coconut or chopped dried fruit instead.\n- These truffles are also delicious dipped in melted chocolate or drizzled with caramel sauce.\n\nEnjoy!"]
  },
  {
    "role": "user",
    "parts": ["i  accidently put too much salt in my pumpkin soup, what should i do now"]
  },
  {
    "role": "model",
    "parts": ["**Here are a few things you can do to fix pumpkin soup that is too salty:**\n\n* **Add a sweetener:** Adding a touch of sweetness can help to balance out the saltiness. Try adding a tablespoon or two of honey, maple syrup, or brown sugar. You could also add a pinch of baking soda, which will help to neutralize the acidity of the tomatoes and reduce the perception of saltiness.\n\n\n* **Add more liquid:** Diluting the soup with more liquid will help to reduce the concentration of salt. You can add water, broth, or even milk. If you add milk, be sure to heat it gently so that it doesn't curdle.\n\n\n* **Add a starchy ingredient:** Starchy ingredients like potatoes, rice, or flour can help to absorb some of the salt. Try adding a peeled and diced potato or a few tablespoons of rice to the soup and simmering until the starch has released. You can also make a slurry by mixing a tablespoon of flour with a little bit of water until it forms a smooth paste, then whisking it into the soup.\n\n\n* **Add an acidic ingredient:** Acidic ingredients like lemon juice, vinegar, or yogurt can help to cut through the saltiness. Start by adding a small amount and taste the soup as you go. Be careful not to add too much acid, or the soup will become too sour.\n\n\n* **Serve with a salty topping:** If all else fails, you can try serving the soup with a salty topping, such as crumbled bacon, grated Parmesan cheese, or sour cream. This will help to balance out the flavors and make the soup more palatable.\n\n**Here is a specific recipe that you can try:**\n\n**Ingredients:**\n\n- 1 batch of pumpkin soup, too salty\n- 1-2 tablespoons honey, maple syrup, or brown sugar\n- 1 cup water, broth, or milk\n- 1 peeled and diced potato (optional)\n- 1 tablespoon flour (optional)\n- 1 tablespoon water (optional)\n- 1 tablespoon lemon juice, vinegar, or yogurt (optional)\n- Salt and pepper to taste\n\n**Instructions:**\n\n1. Bring the pumpkin soup to a simmer in a large pot.\n2. Add the honey, maple syrup, or brown sugar and stir to dissolve.\n3. Add the water, broth, or milk and bring the soup back to a simmer.\n4. If using, add the diced potato and simmer until tender, about 10 minutes.\n5. If using, make a slurry by mixing the flour and water until smooth. Slowly whisk the slurry into the soup, stirring constantly. Bring the soup to a simmer and cook for 1-2 minutes, or until thickened.\n6. If using, add the lemon juice, vinegar, or yogurt and stir to combine.\n7. Taste the soup and season with additional salt and pepper as needed.\n8. Serve immediately.\n\n**Tips:**\n\n- If you are using a store-bought pumpkin soup, be sure to check the label for the sodium content. Some brands of pumpkin soup can be quite high in sodium.\n- If you are making your own pumpkin soup, be careful not to add too much salt when seasoning the soup. You can always add more salt later, but it is difficult to remove salt from a soup.\n- If you are using a starchy ingredient to absorb the salt, be sure to simmer the soup for long enough to allow the starch to release.\n- If you are using an acidic ingredient to cut through the saltiness, be careful not to add too much or the soup will become too sour.\n- Serve the soup with a salty topping, such as crumbled bacon, grated Parmesan cheese, or sour cream, to help balance out the flavors."]
  },
  {
    "role": "user",
    "parts": ["how do i make a sweet using just milk, heavy cream, sugar and butter"]
  },
  {
    "role": "model",
    "parts": ["**Milk Caramel Sauce**\n\n**Ingredients:**\n\n- 1 cup granulated sugar\n- 1/4 cup water\n- 1 cup whole milk\n- 1/2 cup heavy cream\n- 1 tablespoon unsalted butter, cut into small pieces\n- 1/2 teaspoon vanilla extract\n\n**Instructions:**\n\n1. In a medium saucepan, combine the sugar and water. Bring to a simmer over medium heat, stirring constantly to dissolve the sugar.\n2. Once the sugar has dissolved, stop stirring and let the mixture simmer gently. The sugar will start to turn a light amber color.\n3. Continue to simmer the sugar mixture, swirling the pan occasionally, until it reaches a deep amber color. This will take about 5-7 minutes.\n4. Once the sugar mixture is a deep amber color, remove it from the heat and carefully whisk in the milk. Be careful, as the mixture will bubble up vigorously.\n5. Return the saucepan to the heat and bring the mixture to a simmer. Cook for 5 minutes, stirring constantly.\n6. Remove the saucepan from the heat and stir in the heavy cream, butter, and vanilla extract.\n7. Let the caramel sauce cool for a few minutes, then transfer it to a jar or container.\n8. Store the caramel sauce in the refrigerator for up to 2 weeks.\n\n**To use the caramel sauce:**\n\n- Drizzle it over ice cream, pancakes, waffles, or French toast.\n- Use it as a filling for cakes, pies, or tarts.\n- Stir it into coffee or hot chocolate.\n- Use it as a glaze for roasted vegetables or grilled meats.\n\n**Tips:**\n\n- Be careful not to overcook the sugar mixture, or it will become bitter.\n- If you want a thicker caramel sauce, simmer it for a few minutes longer.\n- You can also add other flavorings to the caramel sauce, such as cinnamon, nutmeg, or ginger.\n- If the caramel sauce is too thick, you can thin it out with a little bit of milk or cream.\n\nEnjoy!"]
  },
  {
    "role": "user",
    "parts": ["make a fudge using those ingrediants"]
  },
  {
    "role": "model",
    "parts": ["**Milk Chocolate Fudge**\n\n**Ingredients:**\n\n- 1 cup granulated sugar\n- 1/2 cup milk\n- 1/4 cup heavy cream\n- 1 tablespoon unsalted butter, cut into small pieces\n- 1/2 teaspoon vanilla extract\n- 6 ounces semisweet chocolate, finely chopped\n\n**Instructions:**\n\n1. In a medium saucepan, combine the sugar, milk, and heavy cream. Bring to a simmer over medium heat, stirring constantly to dissolve the sugar.\n2. Once the sugar has dissolved, stop stirring and let the mixture simmer gently. The sugar will start to turn a light amber color.\n3. Continue to simmer the sugar mixture, swirling the pan occasionally, until it reaches a deep amber color. This will take about 5-7 minutes.\n4. Once the sugar mixture is a deep amber color, remove it from the heat and carefully whisk in the butter. Be careful, as the mixture will bubble up vigorously.\n5. Return the saucepan to the heat and bring the mixture to a simmer. Cook for 5 minutes, stirring constantly.\n6. Remove the saucepan from the heat and stir in the vanilla extract and chocolate. Stir until the chocolate is completely melted and smooth.\n7. Pour the fudge mixture into an 8x8 inch baking dish lined with parchment paper.\n8. Let the fudge cool for at least 2 hours, or until it is firm.\n9. Cut the fudge into squares and enjoy!\n\n**Tips:**\n\n- Be careful not to overcook the sugar mixture, or it will become bitter.\n- If you want a thicker fudge, simmer it for a few minutes longer.\n- You can also add other flavorings to the fudge, such as nuts, dried fruit, or spices.\n- If the fudge is too thick, you can thin it out with a little bit of milk or cream.\n\nEnjoy!"]
  },
  {
    "role": "user",
    "parts": ["what texture should the mixture be before putting it in the mold"]
  },
  {
    "role": "model",
    "parts": ["The mixture should be thick and glossy, and it should hold its shape when you pour it. It should not be too runny, or it will not set properly in the mold. If the mixture is too thick, you can thin it out with a little bit of milk or cream.\n\nTo test the consistency of the fudge mixture, you can drop a small amount of it into a glass of cold water. If the fudge forms a soft ball that holds its shape, it is ready to be poured into the mold. If the fudge dissolves in the water, it needs to be cooked for a few minutes longer.\n\nHere is a more detailed description of the different stages of fudge:\n\n* **Soft-ball stage:** The mixture will form a soft ball that holds its shape when dropped into cold water. This is the ideal stage for fudge that is to be poured into a mold.\n* **Firm-ball stage:** The mixture will form a firm ball that holds its shape when dropped into cold water. This stage is used for fudge that is to be cut into squares or rolled into balls.\n* **Hard-ball stage:** The mixture will form a hard ball that is difficult to mold when dropped into cold water. This stage is used for fudge that is to be pulled or taffy.\n\nIt is important to note that the cooking time for fudge will vary depending on the type of fudge you are making and the altitude at which you are cooking. Fudge made at higher altitudes will need to be cooked for a shorter amount of time than fudge made at lower altitudes.\n\nOnce the fudge mixture has reached the desired consistency, remove it from the heat and pour it into the prepared mold. Let the fudge cool for at least 2 hours, or until it is firm."]
  },
  {
    "role": "user",
    "parts": ["can i eat glass"]
  },
  {
    "role": "model",
    "parts": ["**No, you cannot eat glass.**\n\nGlass is a sharp and brittle material that can cause serious injury if ingested. It can cut your mouth, throat, and digestive tract. It can also cause internal bleeding and perforation of the intestines. In some cases, eating glass can even be fatal.\n\nThere is no nutritional value in glass, and it cannot be digested by the human body. Eating glass can also lead to a number of health problems, including:\n\n* **Lacerations:** Glass shards can cut your mouth, throat, and digestive tract, causing pain, bleeding, and infection.\n* **Internal bleeding:** Glass shards can puncture your intestines, causing internal bleeding. This can be a life-threatening condition.\n* **Perforation of the intestines:** Glass shards can also perforate your intestines, causing bacteria and other harmful substances to leak into your abdominal cavity. This can lead to infection, sepsis, and even death.\n* **Lead poisoning:** Some types of glass, such as crystal and leaded glass, contain lead. Lead is a toxic metal that can cause a number of health problems, including brain damage, kidney damage, and reproductive problems.\n* **Other health problems:** Eating glass can also lead to other health problems, such as constipation, diarrhea, and abdominal pain.\n\nIf you accidentally swallow a small piece of glass, it is important to seek medical attention immediately. The doctor may recommend an X-ray to determine the location of the glass and may need to remove it surgically.\n\n**Do not attempt to eat glass under any circumstances.** It is a dangerous and potentially life-threatening行為."]
  },
])

#convo.send_message("YOUR_USER_INPUT")
#print(convo.last.text)

# Streamlit app
st.title("Culinary Chatbot")

# User input
user_input = st.text_input("Enter your message:")

# Button to generate response
if st.button("Send"):
    # Add user input to the conversation
    convo.send_message(user_input)

    # Get and display the model's response
    response = convo.last.text
    st.subheader("Chatbot's Response:")
    st.write(response)