"""
Question Flow System for Chat-Based Marketing Plan Generator

Defines structured question sequences for each business category.
Questions are asked one at a time in a conversational flow.
"""

# Question flow definitions for each business category
QUESTION_FLOWS = {
    "restaurant": [
        {
            "id": "business_name",
            "question": "What's your restaurant's name?",
            "type": "text",
            "required": True,
            "help_text": "This will be used throughout your marketing plan"
        },
        {
            "id": "cuisine_type",
            "question": "What type of cuisine do you serve?",
            "type": "text",
            "required": True,
            "help_text": "e.g., Italian, Mexican, Asian fusion, American, etc."
        },
        {
            "id": "location",
            "question": "Where is your restaurant located? (City, State)",
            "type": "text",
            "required": True,
            "help_text": "This helps us understand your local market"
        },
        {
            "id": "target_audience",
            "question": "Who are your ideal customers? Describe them in a few sentences.",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Families with kids, young professionals, date night couples, etc."
        },
        {
            "id": "budget",
            "question": "What's your monthly marketing budget?",
            "type": "select",
            "options": ["Under $500", "$500-1000", "$1000-2500", "$2500-5000", "$5000+"],
            "required": True,
            "help_text": "This helps us recommend the right marketing channels"
        },
        {
            "id": "current_marketing",
            "question": "What marketing are you currently doing? (if any)",
            "type": "textarea",
            "required": False,
            "help_text": "e.g., Social media, Google Ads, word of mouth, etc."
        },
        {
            "id": "biggest_challenge",
            "question": "What's your biggest marketing challenge right now?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Getting new customers, retaining regulars, competing with chains, etc."
        },
        {
            "id": "unique_value",
            "question": "What makes your restaurant special or different?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Family recipes, local ingredients, unique atmosphere, etc."
        },
        {
            "id": "goals",
            "question": "What are your main marketing goals? (e.g., increase foot traffic, launch delivery, etc.)",
            "type": "textarea",
            "required": True,
            "help_text": "Be specific - this shapes your action plan"
        }
    ],
    
    "retail_store": [
        {
            "id": "business_name",
            "question": "What's your store's name?",
            "type": "text",
            "required": True
        },
        {
            "id": "product_category",
            "question": "What type of products do you sell?",
            "type": "text",
            "required": True,
            "help_text": "e.g., Clothing, electronics, home goods, specialty items, etc."
        },
        {
            "id": "location",
            "question": "Where is your store located? (City, State)",
            "type": "text",
            "required": True
        },
        {
            "id": "target_audience",
            "question": "Who are your ideal customers?",
            "type": "textarea",
            "required": True,
            "help_text": "Describe their demographics, interests, and shopping habits"
        },
        {
            "id": "budget",
            "question": "What's your monthly marketing budget?",
            "type": "select",
            "options": ["Under $500", "$500-1000", "$1000-2500", "$2500-5000", "$5000+"],
            "required": True
        },
        {
            "id": "online_presence",
            "question": "Do you sell online, in-store only, or both?",
            "type": "select",
            "options": ["In-store only", "Online only", "Both online and in-store"],
            "required": True
        },
        {
            "id": "biggest_challenge",
            "question": "What's your biggest marketing challenge?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Competing with Amazon, driving foot traffic, seasonal sales, etc."
        },
        {
            "id": "unique_value",
            "question": "What makes your store special?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Curated selection, expert staff, local focus, unique products, etc."
        },
        {
            "id": "goals",
            "question": "What are your main marketing goals?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Increase foot traffic, launch e-commerce, build email list, etc."
        }
    ],
    
    "professional_services": [
        {
            "id": "business_name",
            "question": "What's your business name?",
            "type": "text",
            "required": True
        },
        {
            "id": "service_type",
            "question": "What type of professional services do you offer?",
            "type": "text",
            "required": True,
            "help_text": "e.g., Legal, accounting, consulting, marketing agency, etc."
        },
        {
            "id": "location",
            "question": "Where are you located? (City, State, or 'Remote/Online')",
            "type": "text",
            "required": True
        },
        {
            "id": "target_audience",
            "question": "Who are your ideal clients?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Small businesses, startups, individuals, specific industries, etc."
        },
        {
            "id": "budget",
            "question": "What's your monthly marketing budget?",
            "type": "select",
            "options": ["Under $500", "$500-1000", "$1000-2500", "$2500-5000", "$5000+"],
            "required": True
        },
        {
            "id": "current_clients",
            "question": "How do you currently get most of your clients?",
            "type": "select",
            "options": ["Referrals", "Online search", "Social media", "Networking", "Advertising", "Other"],
            "required": True
        },
        {
            "id": "biggest_challenge",
            "question": "What's your biggest marketing challenge?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Building trust, generating leads, standing out from competitors, etc."
        },
        {
            "id": "unique_value",
            "question": "What makes your services unique or valuable?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Years of experience, specialized expertise, personalized approach, etc."
        },
        {
            "id": "goals",
            "question": "What are your main marketing goals?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Generate more leads, build thought leadership, expand to new markets, etc."
        }
    ],
    
    "ecommerce": [
        {
            "id": "business_name",
            "question": "What's your online store's name?",
            "type": "text",
            "required": True
        },
        {
            "id": "product_category",
            "question": "What products do you sell?",
            "type": "text",
            "required": True,
            "help_text": "e.g., Fashion, electronics, handmade goods, digital products, etc."
        },
        {
            "id": "platform",
            "question": "What platform do you use for your online store?",
            "type": "select",
            "options": ["Shopify", "WooCommerce", "Etsy", "Amazon", "Custom website", "Other"],
            "required": True
        },
        {
            "id": "target_audience",
            "question": "Who are your ideal customers?",
            "type": "textarea",
            "required": True,
            "help_text": "Describe their demographics, interests, and shopping behavior"
        },
        {
            "id": "budget",
            "question": "What's your monthly marketing budget?",
            "type": "select",
            "options": ["Under $500", "$500-1000", "$1000-2500", "$2500-5000", "$5000+"],
            "required": True
        },
        {
            "id": "current_traffic",
            "question": "How do you currently get most of your website traffic?",
            "type": "select",
            "options": ["Organic search", "Social media", "Paid ads", "Email", "Direct", "Other"],
            "required": True
        },
        {
            "id": "biggest_challenge",
            "question": "What's your biggest marketing challenge?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Getting traffic, converting visitors, competing with big brands, etc."
        },
        {
            "id": "unique_value",
            "question": "What makes your products or brand special?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Unique designs, sustainable materials, handmade quality, etc."
        },
        {
            "id": "goals",
            "question": "What are your main marketing goals?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Increase sales, grow email list, expand to new channels, etc."
        }
    ],
    
    "local_services": [
        {
            "id": "business_name",
            "question": "What's your business name?",
            "type": "text",
            "required": True
        },
        {
            "id": "service_type",
            "question": "What services do you provide?",
            "type": "text",
            "required": True,
            "help_text": "e.g., Plumbing, electrical, landscaping, cleaning, home repair, etc."
        },
        {
            "id": "service_area",
            "question": "What area do you serve? (City, County, or specific neighborhoods)",
            "type": "text",
            "required": True,
            "help_text": "This is crucial for local SEO and targeting"
        },
        {
            "id": "target_audience",
            "question": "Who are your ideal customers?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Homeowners, property managers, businesses, etc."
        },
        {
            "id": "budget",
            "question": "What's your monthly marketing budget?",
            "type": "select",
            "options": ["Under $500", "$500-1000", "$1000-2500", "$2500-5000", "$5000+"],
            "required": True
        },
        {
            "id": "current_leads",
            "question": "How do you currently get most of your leads?",
            "type": "select",
            "options": ["Referrals", "Google search", "Angie's List/Yelp", "Social media", "Door hangers/flyers", "Other"],
            "required": True
        },
        {
            "id": "biggest_challenge",
            "question": "What's your biggest marketing challenge?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Standing out from competitors, getting found online, building trust, etc."
        },
        {
            "id": "unique_value",
            "question": "What makes your service special?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Licensed & insured, 20+ years experience, 24/7 availability, etc."
        },
        {
            "id": "goals",
            "question": "What are your main marketing goals?",
            "type": "textarea",
            "required": True,
            "help_text": "e.g., Get more leads, improve online presence, expand service area, etc."
        }
    ]
}


def get_next_question(category, answered_questions):
    """
    Get the next unanswered question in the sequence for a category.
    
    Args:
        category: Business category (e.g., 'restaurant', 'retail_store')
        answered_questions: Dictionary of question_id -> answer pairs
    
    Returns:
        Question dictionary or None if all questions answered
    """
    if category not in QUESTION_FLOWS:
        return None
    
    questions = QUESTION_FLOWS[category]
    
    # Find first unanswered required question, or first unanswered optional question
    for question in questions:
        question_id = question["id"]
        
        # Skip if already answered
        if question_id in answered_questions:
            continue
        
        # Return first unanswered question (prioritize required)
        return question
    
    # All questions answered
    return None


def get_all_questions(category):
    """
    Get all questions for a category.
    
    Args:
        category: Business category
    
    Returns:
        List of question dictionaries
    """
    return QUESTION_FLOWS.get(category, [])


def is_flow_complete(category, answered_questions):
    """
    Check if all required questions for a category are answered.
    
    Args:
        category: Business category
        answered_questions: Dictionary of question_id -> answer pairs
    
    Returns:
        Boolean indicating if flow is complete
    """
    if category not in QUESTION_FLOWS:
        return False
    
    questions = QUESTION_FLOWS[category]
    required_questions = [q for q in questions if q.get("required", True)]
    
    # Check if all required questions are answered
    for question in required_questions:
        if question["id"] not in answered_questions:
            return False
    
    return True


def get_budget_tier(budget_str):
    """Extract budget tier from budget string"""
    if not budget_str:
        return "unknown"
    budget_lower = budget_str.lower()
    # Check in order from highest to lowest to avoid false matches
    if ("$5000" in budget_lower or "$5,000" in budget_lower) and "+" in budget_lower:
        return "high"
    elif "$2500" in budget_lower or "$2,500" in budget_lower or "$5000" in budget_lower or "$5,000" in budget_lower:
        return "medium-high"
    elif "$1000" in budget_lower or "$1,000" in budget_lower:
        return "medium"
    elif "$500" in budget_lower and ("1000" in budget_lower or "1,000" in budget_lower):
        return "low-medium"
    elif "under $500" in budget_lower or "< 500" in budget_lower:
        return "low"
    elif "+" in budget_lower:  # Catch any "+" that wasn't caught above
        return "high"
    return "unknown"


def get_category_insights(category):
    """Get category-specific marketing insights and best practices"""
    insights = {
        "restaurant": {
            "top_channels": ["Google My Business", "Instagram", "Facebook", "Local SEO", "Email Marketing", "Yelp"],
            "quick_wins": ["Optimize Google My Business profile", "Post food photos on Instagram 3x/week", "Collect customer reviews", "Create a simple email newsletter"],
            "common_mistakes": ["Ignoring online reviews", "Inconsistent social media posting", "Not claiming free listings", "Poor food photography"],
            "industry_stats": "Restaurants see 3-5x ROI on local SEO. 60% of diners check reviews before visiting. Instagram food posts get 2x engagement."
        },
        "retail_store": {
            "top_channels": ["Google My Business", "Facebook", "Instagram", "Local SEO", "Email Marketing", "In-store events"],
            "quick_wins": ["Optimize Google My Business", "Post product photos on Instagram", "Start email list", "Create in-store signage"],
            "common_mistakes": ["Not optimizing for local search", "Ignoring social media", "No email capture system", "Poor window displays"],
            "industry_stats": "Local retail stores see 4x ROI on Google Ads. 78% of shoppers research online before buying. Email marketing has $42 ROI per $1 spent."
        },
        "professional_services": {
            "top_channels": ["LinkedIn", "Google Ads", "Content Marketing", "Email Marketing", "Local SEO", "Referral programs"],
            "quick_wins": ["Optimize LinkedIn profile", "Start a simple blog", "Create Google My Business listing", "Ask for referrals"],
            "common_mistakes": ["Not building authority online", "Ignoring LinkedIn", "No content strategy", "Not tracking leads"],
            "industry_stats": "Professional services get 60% of leads from content marketing. LinkedIn generates 3x more leads than other platforms. Referrals convert at 4x higher rate."
        },
        "ecommerce": {
            "top_channels": ["Google Ads", "Facebook/Instagram Ads", "Email Marketing", "SEO", "Influencer Marketing", "Retargeting"],
            "quick_wins": ["Set up Google Shopping", "Start email list", "Optimize product pages for SEO", "Create Facebook pixel"],
            "common_mistakes": ["Not using retargeting", "Poor product descriptions", "No email marketing", "Ignoring mobile optimization"],
            "industry_stats": "E-commerce sees 2.5x ROI on Google Shopping. Email marketing drives 20% of sales. Retargeting converts 10x better than cold traffic."
        },
        "local_services": {
            "top_channels": ["Google My Business", "Google Ads", "Local SEO", "Facebook", "Nextdoor", "Referral programs"],
            "quick_wins": ["Claim Google My Business", "Get 5+ reviews", "Create Facebook page", "Join Nextdoor"],
            "common_mistakes": ["Not claiming free listings", "Ignoring reviews", "No referral system", "Poor website"],
            "industry_stats": "Local services get 64% of leads from Google. Reviews increase conversion by 270%. Referrals are 4x more valuable than other leads."
        }
    }
    return insights.get(category, {
        "top_channels": ["Google My Business", "Social Media", "Email Marketing", "Local SEO"],
        "quick_wins": ["Claim free listings", "Start social media", "Build email list"],
        "common_mistakes": ["Not having online presence", "Inconsistent marketing", "Not tracking results"],
        "industry_stats": "Small businesses that market consistently see 3x more growth."
    })


def get_budget_recommendations(budget_tier):
    """Get channel recommendations based on budget tier"""
    recommendations = {
        "low": {
            "primary_channels": ["Google My Business (Free)", "Social Media (Free)", "Email Marketing (Low cost)", "Local SEO (DIY)"],
            "budget_allocation": "Focus 100% on free/low-cost channels. No paid advertising recommended.",
            "tactics": "Organic social media, email newsletters, local SEO optimization, customer reviews, referral programs"
        },
        "low-medium": {
            "primary_channels": ["Google My Business", "Social Media Ads ($200-300/month)", "Email Marketing", "Local SEO"],
            "budget_allocation": "70% organic/free channels, 30% paid social media ads",
            "tactics": "Facebook/Instagram ads, boosted posts, email marketing, basic SEO, Google My Business optimization"
        },
        "medium": {
            "primary_channels": ["Google Ads ($500-800/month)", "Social Media Ads ($300-500/month)", "Email Marketing", "SEO", "Content Marketing"],
            "budget_allocation": "40% Google Ads, 30% Social Media Ads, 20% SEO/Content, 10% Email/Tools",
            "tactics": "Google Search Ads, Facebook/Instagram campaigns, content creation, email automation, SEO optimization"
        },
        "medium-high": {
            "primary_channels": ["Google Ads ($1000-1500/month)", "Social Media Ads ($500-800/month)", "Email Marketing", "SEO", "Content Marketing", "Retargeting"],
            "budget_allocation": "45% Google Ads, 25% Social Media, 15% SEO/Content, 10% Email, 5% Tools/Analytics",
            "tactics": "Multi-channel campaigns, retargeting, content marketing, email automation, advanced SEO, analytics"
        },
        "high": {
            "primary_channels": ["Google Ads ($2000+/month)", "Social Media Ads ($1000+/month)", "Email Marketing", "SEO", "Content Marketing", "Influencer Marketing", "Retargeting"],
            "budget_allocation": "40% Google Ads, 25% Social Media, 15% SEO/Content, 10% Email, 5% Influencer, 5% Tools/Analytics",
            "tactics": "Full multi-channel strategy, influencer partnerships, advanced retargeting, content production, marketing automation, comprehensive analytics"
        }
    }
    return recommendations.get(budget_tier, recommendations["medium"])


def generate_marketing_plan_prompt(category, answers):
    """
    Generate a structured, intelligent prompt for OpenAI to create a comprehensive marketing plan.
    Includes budget-aware recommendations, category-specific strategies, and industry best practices.
    
    Args:
        category: Business category
        answers: Dictionary of question_id -> answer pairs
    
    Returns:
        String prompt for marketing plan generation
    """
    category_display = category.replace("_", " ").title()
    
    # Get budget tier
    budget_str = answers.get("budget", "")
    budget_tier = get_budget_tier(budget_str)
    budget_recs = get_budget_recommendations(budget_tier)
    
    # Get category-specific insights
    category_insights = get_category_insights(category)
    
    # Build context from answers
    context_sections = []
    
    if "business_name" in answers:
        context_sections.append(f"Business Name: {answers['business_name']}")
    
    if "location" in answers or "service_area" in answers:
        location = answers.get("location") or answers.get("service_area")
        context_sections.append(f"Location/Service Area: {location}")
    
    if "target_audience" in answers:
        context_sections.append(f"Target Audience: {answers['target_audience']}")
    
    if "budget" in answers:
        context_sections.append(f"Monthly Marketing Budget: {answers['budget']} (Budget Tier: {budget_tier})")
    
    if "biggest_challenge" in answers:
        context_sections.append(f"Biggest Challenge: {answers['biggest_challenge']}")
    
    if "unique_value" in answers:
        context_sections.append(f"Unique Value Proposition: {answers['unique_value']}")
    
    if "goals" in answers:
        context_sections.append(f"Marketing Goals: {answers['goals']}")
    
    if "current_marketing" in answers:
        context_sections.append(f"Current Marketing: {answers['current_marketing']}")
    
    # Add category-specific context
    category_context = ""
    if category == "restaurant" and "cuisine_type" in answers:
        category_context = f"\nCuisine Type: {answers['cuisine_type']}"
    elif category == "retail_store" and "product_category" in answers:
        category_context = f"\nProduct Category: {answers['product_category']}"
    elif category == "professional_services" and "service_type" in answers:
        category_context = f"\nService Type: {answers['service_type']}"
    elif category == "ecommerce" and "product_category" in answers:
        category_context = f"\nProduct Category: {answers['product_category']}"
    elif category == "local_services" and "service_type" in answers:
        category_context = f"\nService Type: {answers['service_type']}"
    
    # Build the comprehensive prompt
    prompt = f"""You are an expert marketing consultant with deep knowledge of small business marketing, especially for {category_display} businesses. You're creating a comprehensive, actionable marketing plan.

BUSINESS CONTEXT:
{chr(10).join(context_sections)}{category_context}

INDUSTRY INSIGHTS FOR {category_display.upper()}:
- Top Performing Channels: {', '.join(category_insights['top_channels'])}
- Industry Statistics: {category_insights['industry_stats']}
- Common Mistakes to Avoid: {', '.join(category_insights['common_mistakes'])}

BUDGET-AWARE RECOMMENDATIONS (Budget Tier: {budget_tier}):
- Primary Channels: {', '.join(budget_recs['primary_channels'])}
- Budget Allocation: {budget_recs['budget_allocation']}
- Recommended Tactics: {budget_recs['tactics']}

Create a detailed, actionable marketing plan with the following structure:

## 1. EXECUTIVE SUMMARY
Provide a 2-3 paragraph overview that:
- Summarizes the business and current marketing situation
- Identifies the top 3 opportunities for growth
- Highlights the biggest challenges to address
- Recommends the primary marketing approach based on their budget tier

## 2. TARGET AUDIENCE ANALYSIS
Create detailed customer personas (1-2 personas) that include:
- Demographics (age, income, location, lifestyle)
- Psychographics (values, interests, pain points)
- Where they spend time online and offline
- What messaging and content resonates with them
- How they make purchasing decisions
- Specific to their described target audience: {answers.get('target_audience', 'Not specified')}

## 3. RECOMMENDED MARKETING CHANNELS
Prioritize channels based on their budget ({budget_str}) and audience. For each recommended channel:

**Channel Name** (Priority: High/Medium/Low)
- Why it works for their business and audience
- Specific tactics and strategies (be concrete, not generic)
- Expected monthly cost (if paid)
- Expected ROI or results
- Time commitment required
- Tools/platforms needed

Focus on these channels in priority order: {', '.join(budget_recs['primary_channels'])}

IMPORTANT: If budget is under $500/month, focus heavily on free channels. If over $2500/month, include paid advertising strategies.

## 4. 90-DAY ACTION PLAN
Create a week-by-week breakdown:

**Weeks 1-2: Foundation & Quick Wins**
- Specific tasks to set up core marketing infrastructure
- Quick wins that can show results fast: {', '.join(category_insights['quick_wins'][:2])}
- Tools to set up (Google My Business, email platform, etc.)

**Weeks 3-4: Content & Engagement**
- Content creation tasks
- Social media posting schedule
- Engagement strategies

**Weeks 5-8: Optimization & Expansion**
- What's working? Double down
- What's not? Adjust or stop
- Expand successful tactics

**Weeks 9-12: Scale & Refine**
- Scale what's working
- Refine messaging based on results
- Plan for next quarter

For each week, include:
- Specific tasks (not vague like "do social media" but "post 3 Instagram photos per week featuring behind-the-scenes content")
- Who's responsible (if applicable)
- Expected outcomes
- Tools/resources needed

## 5. SUCCESS METRICS & KPIs
Define measurable goals:
- Primary KPIs (e.g., website traffic, leads, sales, social engagement)
- How to measure each (specific tools/methods)
- Benchmarks for their industry and budget level
- Monthly targets for first 90 days
- How to track and report results

## 6. WHAT TO AVOID (Anti-Patterns)
Based on common mistakes in {category_display} marketing:
- {chr(10).join('- ' + mistake for mistake in category_insights['common_mistakes'])}
- Generic marketing advice that doesn't work
- Tactics that don't match their budget
- Strategies that ignore their specific challenges: {answers.get('biggest_challenge', 'Not specified')}

## 7. NEXT STEPS (Immediate Actions)
List the top 5-7 specific actions they should take THIS WEEK:
1. [Specific, actionable task]
2. [Specific, actionable task]
3. [etc.]

Make each action:
- Specific and concrete
- Achievable within their budget
- Relevant to their goals: {answers.get('goals', 'Not specified')}
- Include tools/resources needed

---

CRITICAL REQUIREMENTS:
1. Be SPECIFIC: Instead of "use social media," say "Post 3x/week on Instagram with behind-the-scenes photos, use these hashtags: [specific hashtags], engage with followers daily"
2. Be BUDGET-AWARE: Don't recommend expensive tools if budget is low. Don't recommend only free tools if budget is high.
3. Be ACTIONABLE: Every recommendation should have clear next steps
4. Be REALISTIC: Don't promise unrealistic results. Set achievable expectations.
5. Be CATEGORY-SPECIFIC: Use {category_display} industry best practices
6. Address their CHALLENGES: Specifically address: {answers.get('biggest_challenge', 'Not specified')}
7. Leverage their STRENGTHS: Build on: {answers.get('unique_value', 'Not specified')}

Format the response with clear markdown headers (## for main sections, ### for subsections). Use bullet points, numbered lists, and bold text for emphasis. Make it scannable and easy to read."""
    
    return prompt


def extract_answer_from_message(message, question):
    """
    Extract structured answer from user's conversational message.
    This is a helper function that can be enhanced with NLP if needed.
    
    Args:
        message: User's message text
        question: Question dictionary
    
    Returns:
        Extracted answer (string)
    """
    # For now, return the message as-is
    # In future, could add NLP to extract specific information
    return message.strip()

