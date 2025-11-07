import React from 'react';
import '../styles/CategorySelector.css';

const BUSINESS_CATEGORIES = [
  {
    id: 'restaurant',
    name: 'Restaurant',
    icon: '🍽️',
    description: 'Cafes, fine dining, fast casual, food trucks',
    type: 'business'
  },
  {
    id: 'retail_store',
    name: 'Retail Store',
    icon: '🛍️',
    description: 'Boutiques, specialty shops, brick & mortar',
    type: 'business'
  },
  {
    id: 'professional_services',
    name: 'Professional Services',
    icon: '💼',
    description: 'Consulting, legal, accounting, agencies',
    type: 'business'
  },
  {
    id: 'ecommerce',
    name: 'E-commerce',
    icon: '🛒',
    description: 'Online stores, marketplaces, digital products',
    type: 'business'
  },
  {
    id: 'local_services',
    name: 'Local Services',
    icon: '🔧',
    description: 'Plumbers, electricians, contractors, home services',
    type: 'business'
  }
];

const MARKETING_GOAL_CATEGORIES = [
  {
    id: 'increase_sales',
    name: 'Increase Sales',
    icon: '📈',
    description: 'Convert more prospects into paying customers',
    type: 'marketing_goal'
  },
  {
    id: 'build_brand_awareness',
    name: 'Build Brand Awareness',
    icon: '🎯',
    description: 'Get more people to recognize your brand',
    type: 'marketing_goal'
  },
  {
    id: 'generate_more_leads',
    name: 'Generate More Leads',
    icon: '🎁',
    description: 'Attract qualified prospects interested in your products',
    type: 'marketing_goal'
  },
  {
    id: 'drive_foot_traffic',
    name: 'Drive Foot Traffic',
    icon: '🚶',
    description: 'Get more customers through your physical location',
    type: 'marketing_goal'
  },
  {
    id: 'retain_customers',
    name: 'Retain Customers',
    icon: '🔁',
    description: 'Encourage repeat purchases and build loyalty',
    type: 'marketing_goal'
  },
  {
    id: 'launch_new_service_product',
    name: 'Launch New Service / Product',
    icon: '🎉',
    description: 'Generate excitement and attract early adopters',
    type: 'marketing_goal'
  }
];

function CategorySelector({ onSelectCategory }) {
  const [selectedType, setSelectedType] = React.useState('business'); // 'business' or 'marketing_goal'

  const handleTypeSelect = (type) => {
    setSelectedType(type);
  };

  const categories = selectedType === 'business' ? BUSINESS_CATEGORIES : MARKETING_GOAL_CATEGORIES;

  return (
    <div className="category-selector-page">
      <div className="category-container">
        <header className="category-header">
          <h1>What do you need help with?</h1>
          <p className="category-subtitle">
            Choose your business type or marketing goal to get personalized guidance
          </p>
        </header>

        {/* Type Selector Tabs */}
        <div className="category-type-selector">
          <button
            className={`type-tab ${selectedType === 'business' ? 'active' : ''}`}
            onClick={() => handleTypeSelect('business')}
            type="button"
          >
            Business Type
          </button>
          <button
            className={`type-tab ${selectedType === 'marketing_goal' ? 'active' : ''}`}
            onClick={() => handleTypeSelect('marketing_goal')}
            type="button"
          >
            Marketing Goal
          </button>
        </div>

        <div className="category-grid">
          {categories.map((category) => (
            <button
              key={category.id}
              className="category-card"
              onClick={() => onSelectCategory(category.id)}
              type="button"
            >
              <div className="category-icon">{category.icon}</div>
              <h3 className="category-name">{category.name}</h3>
              <p className="category-description">{category.description}</p>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}

export default CategorySelector;

