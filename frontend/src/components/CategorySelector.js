import React from 'react';
import '../styles/CategorySelector.css';

const BUSINESS_CATEGORIES = [
  {
    id: 'restaurant',
    name: 'Restaurant',
    icon: '🍽️',
    description: 'Cafes, fine dining, fast casual, food trucks'
  },
  {
    id: 'retail_store',
    name: 'Retail Store',
    icon: '🛍️',
    description: 'Boutiques, specialty shops, brick & mortar'
  },
  {
    id: 'professional_services',
    name: 'Professional Services',
    icon: '💼',
    description: 'Consulting, legal, accounting, agencies'
  },
  {
    id: 'ecommerce',
    name: 'E-commerce',
    icon: '🛒',
    description: 'Online stores, marketplaces, digital products'
  },
  {
    id: 'local_services',
    name: 'Local Services',
    icon: '🔧',
    description: 'Plumbers, electricians, contractors, home services'
  }
];

function CategorySelector({ onSelectCategory }) {
  return (
    <div className="category-selector-page">
      <div className="category-container">
        <header className="category-header">
          <h1>What type of business are you?</h1>
          <p className="category-subtitle">
            Select your category to get a personalized marketing plan
          </p>
        </header>

        <div className="category-grid">
          {BUSINESS_CATEGORIES.map((category) => (
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

