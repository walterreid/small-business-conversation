import React, { useState } from 'react';
import { generateTemplate } from './api';
import './App.css';

// Example queries to help users understand how to write good prompts
const EXAMPLE_QUERIES = {
  groomsman: {
    domain: "I need to write a groomsman speech for my best friend's wedding. I want it to be heartfelt and funny, but not embarrassing. We've been friends since college and have been through a lot together.",
    framing: "I'm not great at public speaking and tend to ramble. I want something that feels authentic, not like I copied it from the internet."
  },
  performance: {
    domain: "I need to write a performance review for a junior developer on my team. They're talented but struggle with time management and asking for help when stuck.",
    framing: "I want to be constructive and encouraging, not critical. Focus on growth, not problems. They're early in their career and I don't want to discourage them."
  },
  apology: {
    domain: "I need to apologize to a friend I hurt by canceling plans last minute for the third time. I have legitimate reasons but I know it's been a pattern and they're rightfully upset.",
    framing: "I don't want to make excuses or justify my behavior. I want to take real accountability and show I understand the impact, not just my intent."
  },
  vows: {
    domain: "I need help writing wedding vows to my partner. We've been together 5 years and I want them to feel personal and specific, not generic.",
    framing: "I'm not naturally romantic or poetic. I want something that sounds like me - honest, a little funny, deeply sincere. Avoid clichés like 'journey' and 'soulmate'."
  },
  email: {
    domain: "I need to write a difficult email to a client explaining why their project is delayed. The delay is partly our fault (scope creep we should have managed better) and partly theirs (late feedback, changing requirements).",
    framing: "I want to be honest without being defensive. Acknowledge our part, explain the situation clearly, and propose a solution. Professional but human."
  },
  explainCode: {
    domain: "I have existing code I didn't write and need to understand how it works. I know basic programming but this codebase uses patterns I'm not familiar with and has unclear variable names.",
    framing: "I'm going to share you some javascript code in my next chat prompt.  I'd then like you to step-by-step walkthrough it. Explaining the logic, patterns, and why certain design choices were made."
  },
  learnMath: {
    domain: "I need help understanding compound interest and how it applies to loans and investments. I understand basic percentages but don't get why time matters so much.",
    framing: "I learn best with real-world examples and visual explanations. I want to actually understand the math, not just memorize formulas."
  }
};

// Loading tips to educate users while waiting
const LOADING_TIPS = [
  "🎯 Good prompts specify what to avoid, not just what to include...",
  "💡 The more specific your input, the better the output...",
  "🚀 Anti-patterns help AI avoid generic responses...",
  "✨ Concrete examples beat abstract instructions every time...",
  "🎭 'First draft' language reduces perfectionism and helps you start...",
  "🔍 Variables capture what makes your situation unique...",
  "🎨 Philosophical grounding shapes how AI approaches your task...",
  "📝 Constraints prevent rambling and force focus on what matters...",
  "💬 The best prompts feel like conversations, not commands...",
  "⚡ Specificity > Length. Short + concrete beats long + vague...",
  "🎯 We're teaching the AI what 'good' looks like for YOUR situation...",
  "🔧 Building your personalized prompt template brick by brick...",
  "🎨 Crafting questions that prevent cookie-cutter output...",
  "🧠 Did you know? The best prompts embed 'lived understanding' not theory...",
  "🎪 Fun fact: This system uses a meta-prompt to generate your prompt...",
];

function App() {
  // State management
  const [step, setStep] = useState(1); // 1: Landing, 2: Loading, 3: Form, 4: Result
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [retryCount, setRetryCount] = useState(0);
  const [lastErrorType, setLastErrorType] = useState('');
  
  // Form data
  const [userDomain, setUserDomain] = useState('');
  const [userFraming, setUserFraming] = useState('');
  const [templateData, setTemplateData] = useState(null);
  const [schema, setSchema] = useState(null);
  const [formValues, setFormValues] = useState({});
  const [finalPrompt, setFinalPrompt] = useState('');
  const [copySuccess, setCopySuccess] = useState(false);
  const [showDebug, setShowDebug] = useState(false);
  const [feedbackGiven, setFeedbackGiven] = useState(false);
  const [feedbackType, setFeedbackType] = useState(null);
  const [showExample, setShowExample] = useState(false);
  const [exampleOutput, setExampleOutput] = useState('');
  const [generatingExample, setGeneratingExample] = useState(false);
  const [currentTip, setCurrentTip] = useState(0);
  const [tipInterval, setTipInterval] = useState(null);
  const [showExampleHint, setShowExampleHint] = useState(false);
  const [showContextField, setShowContextField] = useState(false);
  const [showFastModeDialog, setShowFastModeDialog] = useState(false);

  // Load example query to help users understand good prompts
  const loadExample = (exampleKey) => {
    const example = EXAMPLE_QUERIES[exampleKey];
    if (example) {
      setUserDomain(example.domain);
      setUserFraming(example.framing);
      clearError();
      
      // Auto-expand additional context if it has content
      if (example.framing) {
        setShowContextField(true);
      }
      
      // Show hint after loading example
      setShowExampleHint(true);
      setTimeout(() => setShowExampleHint(false), 5000);
      
      // Scroll to input section
      const inputSection = document.querySelector('.form-section');
      if (inputSection) {
        inputSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  };

  // Error handling utilities
  const logError = (errorType, error, context = {}) => {
    console.error(`[${errorType}]`, error, context);
    setLastErrorType(errorType);
  };

  const getUserFriendlyMessage = (errorType, error) => {
    const messages = {
      'network': {
        message: 'Unable to connect to the server.',
        suggestion: 'Check your internet connection and try again. If the problem persists, the service may be temporarily down.'
      },
      'api_key': {
        message: 'API configuration error.',
        suggestion: 'Please contact support. This is not an issue with your input.'
      },
      'rate_limit': {
        message: 'Too many requests.',
        suggestion: 'Please wait a moment and try again. The service has usage limits to ensure quality for all users.'
      },
      'timeout': {
        message: 'The request took too long.',
        suggestion: 'Try again, or try simplifying your request slightly. Complex requests sometimes need multiple attempts.'
      },
      'parsing': {
        message: 'The AI returned an unexpected format.',
        suggestion: 'This usually means the request was too vague or unusual. Try adding more specific details about what you need help with. Check the examples below for guidance.'
      },
      'validation': {
        message: error.message || 'Please check your input.',
        suggestion: 'Make sure your request is at least 10 characters and describes what you need help with.'
      },
      'unknown': {
        message: 'An unexpected error occurred.',
        suggestion: 'Please try again. If the problem persists, try using one of the example queries to ensure the format is correct.'
      }
    };

    // Check for specific error patterns
    if (error.message?.includes('fetch')) {
      return `${messages.network.message} ${messages.network.suggestion}`;
    }
    if (error.message?.includes('API key')) {
      return `${messages.api_key.message} ${messages.api_key.suggestion}`;
    }
    if (error.message?.includes('rate limit')) {
      return `${messages.rate_limit.message} ${messages.rate_limit.suggestion}`;
    }
    if (error.message?.includes('timeout')) {
      return `${messages.timeout.message} ${messages.timeout.suggestion}`;
    }
    if (error.message?.includes('parse')) {
      return `${messages.parsing.message} ${messages.parsing.suggestion}`;
    }
    
    const errorInfo = messages[errorType] || messages.unknown;
    return `${errorInfo.message} ${errorInfo.suggestion}`;
  };

  const handleError = (errorType, error, context = {}) => {
    logError(errorType, error, context);
    setError(getUserFriendlyMessage(errorType, error));
    setLoading(false);
  };

  const clearError = () => {
    setError('');
    setLastErrorType('');
    setRetryCount(0);
  };

  const canRetry = (errorType) => {
    const retryableErrors = ['network', 'timeout', 'rate_limit', 'parsing'];
    return retryableErrors.includes(errorType) && retryCount < 3;
  };

  const handleRetry = () => {
    setRetryCount(prev => prev + 1);
    clearError();
    handleGenerateTemplate();
  };

  // Extract sample text from the field's placeholder (provided by AI)
  const generateSampleText = (field) => {
    // The AI provides sample text in the Placeholder field of each question
    // This is the sample text that should be used for the "Use Sample" button
    if (field.placeholder && field.placeholder.trim()) {
      console.log('Using placeholder as sample text for field:', field.id, 'placeholder:', field.placeholder);
      return field.placeholder.trim();
    }
    
    // Fallback if no placeholder is provided
    console.log('No placeholder found for field:', field.id);
    return 'Sample text';
  };

  const handleUseSample = (fieldId) => {
    const field = schema?.formFields?.find(f => f.id === fieldId);
    if (field) {
      if (field.type === 'select' && field.options && field.options.length > 0) {
        // For select fields, use the first option's value
        const firstOptionValue = field.options[0].value;
        handleFieldChange(fieldId, firstOptionValue);
      } else {
        // For text and textarea fields, use the sample text
        const sampleText = generateSampleText(field);
        handleFieldChange(fieldId, sampleText);
      }
    }
  };

  // Handle "Add Relevant Detail" button - scroll to form
  const handleAddRelevantDetail = () => {
    const formSection = document.querySelector('.form-column');
    if (formSection) {
      formSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  };

  // Handle "Fast Mode" button - show dialog
  const handleFastModeClick = () => {
    setShowFastModeDialog(true);
  };

  // Handle "Got it" in Fast Mode dialog
  const handleFastModeConfirm = () => {
    // Fill all fields with sample/default values
    const formValues = {};
    schema?.formFields?.forEach(field => {
      if (field.type === 'select' && field.options && field.options.length > 0) {
        formValues[field.id] = field.options[0].value;
      } else {
        formValues[field.id] = generateSampleText(field);
      }
    });
    
    setFormValues(formValues);
    setShowFastModeDialog(false);
    
    // Scroll to submit button
    const generateButton = document.querySelector('.generate-button');
    if (generateButton) {
      setTimeout(() => {
        generateButton.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 100);
    }
  };

  // Handle "Cancel" in Fast Mode dialog
  const handleFastModeCancel = () => {
    setShowFastModeDialog(false);
  };

  // Parse AI output into structured schema
  const parseAIOutput = (rawOutput, domain, framing) => {
    try {
      console.log('Parsing AI output:', rawOutput);
      
      // Validate input
      if (!rawOutput || typeof rawOutput !== 'string') {
        throw new Error('Invalid AI output: empty or not a string');
      }

      // Check for required sections (with brackets OR markdown bold)
      const hasPromptTemplate = /\[PROMPT_TEMPLATE\]|\*\*PROMPT_TEMPLATE:\*\*/i.test(rawOutput);
      const hasUserQuestions = /\[USER_QUESTIONS\]|\*\*USER_QUESTIONS:\*\*/i.test(rawOutput);

      if (!hasPromptTemplate) {
        throw new Error('Missing [PROMPT_TEMPLATE] or **PROMPT_TEMPLATE:** section in AI response');
      }
      if (!hasUserQuestions) {
        throw new Error('Missing [USER_QUESTIONS] or **USER_QUESTIONS:** section in AI response');
      }

      // Extract anti-patterns (with brackets OR markdown bold)
      const antiPatternsMatch = rawOutput.match(/(?:\[ANTI-PATTERNS\]|\*\*ANTI-PATTERNS:\*\*)([\s\S]*?)(?=\[PROMPT_TEMPLATE\]|\*\*PROMPT_TEMPLATE:\*\*|$)/i);
      const antiPatterns = antiPatternsMatch 
        ? antiPatternsMatch[1]
            .split('\n')
            .filter(line => line.trim().startsWith('-'))
            .map(line => line.trim().substring(1).trim())
            .filter(pattern => pattern.length > 0)
        : [];

      // Extract prompt template (with brackets OR markdown bold)
      const templateMatch = rawOutput.match(/(?:\[PROMPT_TEMPLATE\]|\*\*PROMPT_TEMPLATE:\*\*)([\s\S]*?)(?=\[USER_QUESTIONS\]|\*\*USER_QUESTIONS:\*\*|$)/i);
      let promptTemplate = templateMatch ? templateMatch[1].trim() : '';

      if (!promptTemplate) {
        throw new Error('Empty prompt template in AI response');
      }

      // Add anti-patterns to the prompt template
      if (antiPatterns.length > 0) {
        const antiPatternsText = antiPatterns.map(pattern => `- ${pattern}`).join('\n');
        promptTemplate += `\n\nAnti-patterns to avoid:\n${antiPatternsText}`;
      }

      // Extract user questions/form fields (with brackets OR markdown bold)
      const questionsMatch = rawOutput.match(/(?:\[USER_QUESTIONS\]|\*\*USER_QUESTIONS:\*\*)([\s\S]*?)$/i);
      const questionsSection = questionsMatch ? questionsMatch[1] : '';
      
      if (!questionsSection.trim()) {
        throw new Error('Empty user questions section in AI response');
      }
      
      // Parse individual form fields
      const formFields = [];
      const fieldBlocks = questionsSection.split(/(?=Variable:)/).filter(block => block.trim());

      if (fieldBlocks.length === 0) {
        throw new Error('No form fields found in user questions section');
      }

      fieldBlocks.forEach((block, index) => {
        try {
          const lines = block.trim().split('\n').map(line => line.trim()).filter(line => line);
          
          if (lines.length === 0) return;
          
          let field = {
            id: '',
            variable: '',
            question: '',
            type: 'text',
            placeholder: '',
            options: [],
            helpText: '',
            required: true
          };
          
          lines.forEach(line => {
            console.log('Processing line:', line);
            
            // Extract variable name
            if (line.startsWith('Variable:')) {
              const variableMatch = line.match(/Variable:\s*\{\{([^}]+)\}\}/);
              if (variableMatch) {
                field.variable = `{{${variableMatch[1]}}}`;
                field.id = variableMatch[1];
                console.log('Found variable:', field.id);
              }
            }
            // Extract question
            else if (line.startsWith('Question:')) {
              field.question = line.replace(/Question:\s*["']?/, '').replace(/["']$/, '');
              console.log('Found question:', field.question);
            }
            // Extract type
            else if (line.startsWith('Type:')) {
              const typeMatch = line.match(/Type:\s*(\w+)/);
              if (typeMatch) {
                field.type = typeMatch[1].toLowerCase();
                console.log('Found type:', field.type);
              }
            }
            // Extract placeholder/options
            else if (line.startsWith('Placeholder/Options:') || line.startsWith('Placeholder:') || line.startsWith('Options:')) {
              const content = line.replace(/Placeholder(?:\/Options)?:\s*["']?/, '').replace(/Options:\s*["']?/, '').replace(/["']$/, '');
              console.log('Found options/placeholder content:', content);
              
              if (field.type === 'select') {
                // Parse select options (format: "option1 | option2 | option3")
                field.options = content.split(/\s*\|\s*/)
                  .map(option => ({
                    value: option.trim(),
                    label: option.trim()
                  }))
                  .filter(option => option.value.length > 0);
                
                console.log('Parsed select options:', field.options);
              } else {
                field.placeholder = content;
                console.log('Set placeholder:', field.placeholder);
              }
            }
            // Extract help text
            else if (line.startsWith('Why it matters:')) {
              field.helpText = line.replace(/Why it matters:\s*["']?/, '').replace(/["']$/, '');
              console.log('Found help text:', field.helpText);
            }
          });
          
          // Validate field before adding
          if (!field.id || !field.question) {
            console.warn(`Skipping invalid field at index ${index}:`, field);
            return;
          }

          formFields.push(field);
        } catch (fieldError) {
          console.warn(`Error parsing field at index ${index}:`, fieldError);
          // Continue with other fields
        }
      });

      if (formFields.length === 0) {
        throw new Error('No valid form fields could be parsed from AI response');
      }

      const parsedSchema = {
        domain,
        framing,
        antiPatterns,
        promptTemplate,
        formFields,
        rawOutput
      };

      console.log('Parsed schema:', parsedSchema);
      return parsedSchema;

    } catch (error) {
      console.error('Error parsing AI output:', error);
      throw new Error(`Parsing failed: ${error.message}`);
    }
  };

  // Handle template generation
  const handleGenerateTemplate = async () => {
    // Input validation
    if (!userDomain.trim()) {
      handleError('validation', new Error('Domain is required'), { userDomain, userFraming });
      return;
    }

    if (userDomain.trim().length < 10) {
      handleError('validation', new Error('Please provide more detail about what you need help with'), { userDomain, userFraming });
      return;
    }

    setLoading(true);
    clearError();
    setStep(2);

    // Start rotating tips
    const interval = setInterval(() => {
      setCurrentTip(prev => (prev + 1) % LOADING_TIPS.length);
    }, 3000); // Rotate every 3 seconds
    setTipInterval(interval);

    try {
      console.log('Starting template generation', { 
        userDomain: userDomain.substring(0, 100), 
        userFraming: userFraming?.substring(0, 100),
        retryCount
      });

      const response = await generateTemplate(userDomain, userFraming);
      
      if (response.success) {
        console.log('Template generated successfully', { 
          outputLength: response.output?.length,
          metadata: response.metadata 
        });

        setTemplateData(response);
        
        try {
          // Parse the AI output
          const parsedSchema = parseAIOutput(response.output, userDomain, userFraming);
          setSchema(parsedSchema);
          setStep(3);
          clearError(); // Clear any previous errors on success
          if (tipInterval) clearInterval(tipInterval);
        } catch (parseError) {
          handleError('parsing', parseError, { 
            rawOutput: response.output?.substring(0, 500),
            outputLength: response.output?.length 
          });
          setStep(1);
          if (tipInterval) clearInterval(tipInterval);
        }
      } else {
        handleError('api_response', new Error(response.message || 'API returned unsuccessful response'), { 
          response,
          userDomain: userDomain.substring(0, 100) 
        });
        setStep(1);
        if (tipInterval) clearInterval(tipInterval);
      }
    } catch (error) {
      // Determine error type based on error characteristics
      let errorType = 'unknown';
      
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        errorType = 'network';
      } else if (error.message?.includes('API key')) {
        errorType = 'api_key';
      } else if (error.message?.includes('rate limit')) {
        errorType = 'rate_limit';
      } else if (error.message?.includes('timeout')) {
        errorType = 'timeout';
      } else if (error.message?.includes('parse')) {
        errorType = 'parsing';
      }

      handleError(errorType, error, { 
        userDomain: userDomain.substring(0, 100),
        retryCount,
        errorName: error.name,
        errorMessage: error.message
      });
      setStep(1);
      if (tipInterval) clearInterval(tipInterval);
    } finally {
      setLoading(false);
      if (tipInterval) clearInterval(tipInterval);
    }
  };

  // Handle user feedback
  const handleFeedback = async (type) => {
    setFeedbackType(type);
    setFeedbackGiven(true);
    
    // Log to console for now (can be backend endpoint later)
    console.log('Feedback received:', {
      type,
      domain: userDomain,
      timestamp: new Date().toISOString(),
      fieldsCount: schema?.formFields?.length
    });
    
    // Optional: Send to backend if you add a feedback endpoint
    try {
      const API_BASE_URL = process.env.REACT_APP_API_URL || '';
      await fetch(`${API_BASE_URL}/api/feedback`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          type,
          domain: userDomain,
          metadata: {
            fieldsCount: schema?.formFields?.length,
            timestamp: new Date().toISOString()
          }
        })
      }).catch(() => {
        // Silently fail - feedback is nice-to-have
        console.log('Feedback sent to backend failed (optional)');
      });
    } catch (err) {
      // Silently fail
    }
  };

  // Handle "Try This Prompt" button
  const handleTryPrompt = async () => {
    if (!finalPrompt) return;
    
    setGeneratingExample(true);
    setShowExample(true);
    
    try {
      // Call OpenAI with the filled prompt
      const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000';
      const response = await fetch(`${API_BASE_URL}/api/try-prompt`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
          prompt: finalPrompt
        })
      });
      
      if (!response.ok) {
        throw new Error('Failed to generate example');
      }
      
      const data = await response.json();
      
      if (data.success) {
        setExampleOutput(data.output);
      } else {
        setExampleOutput('Failed to generate example. Please try copying the prompt and using it directly in ChatGPT or Claude.');
      }
    } catch (error) {
      console.error('Example generation failed:', error);
      setExampleOutput('Failed to generate example. Please try copying the prompt and using it directly in ChatGPT or Claude.');
    } finally {
      setGeneratingExample(false);
    }
  };

  // Reset to start over
  const handleStartOver = () => {
    setStep(1);
    setUserDomain('');
    setUserFraming('');
    setTemplateData(null);
    setSchema(null);
    setFormValues({});
    setFinalPrompt('');
    setCopySuccess(false);
    clearError(); // Use clearError to reset all error states
    setShowDebug(false);
    setRetryCount(0);
    setLastErrorType('');
    setFeedbackGiven(false);
    setFeedbackType(null);
    setShowExample(false);
    setExampleOutput('');
    setGeneratingExample(false);
    setCurrentTip(0);
    setShowExampleHint(false);
    if (tipInterval) {
      clearInterval(tipInterval);
      setTipInterval(null);
    }
  };

  // Handle form field changes
  const handleFieldChange = (fieldId, value) => {
    setFormValues(prev => ({
      ...prev,
      [fieldId]: value
    }));
  };

  // Validate form and submit
  const handleFormSubmit = (e) => {
    e.preventDefault();
    
    try {
      // Validate schema exists
      if (!schema || !schema.formFields) {
        handleError('validation', new Error('Form data is missing'), { schema: !!schema, formFields: schema?.formFields?.length });
        return;
      }

      // Validate required fields
      const missingFields = schema.formFields
        .filter(field => field.required && (!formValues[field.id] || formValues[field.id].trim() === ''))
        .map(field => field.question);

      if (missingFields.length > 0) {
        handleError('validation', new Error(`Missing required fields: ${missingFields.join(', ')}`), { 
          missingFields,
          formValues: Object.keys(formValues),
          totalFields: schema.formFields.length 
        });
        return;
      }

      // Clear any previous errors
      clearError();
      
      // Fill the template with user values
      const filledPrompt = fillTemplate(schema.promptTemplate, formValues);
      
      if (!filledPrompt || filledPrompt.trim() === '') {
        handleError('template_filling', new Error('Failed to generate final prompt'), { 
          templateLength: schema.promptTemplate?.length,
          formValuesCount: Object.keys(formValues).length 
        });
        return;
      }

      // Check for unreplaced variables
      const unreplacedVars = filledPrompt.match(/\{\{[^}]+\}\}/g);
      if (unreplacedVars && unreplacedVars.length > 0) {
        handleError('template_filling', new Error(`Some variables were not replaced: ${unreplacedVars.join(', ')}`), { 
          unreplacedVars,
          filledPrompt: filledPrompt.substring(0, 200) 
        });
        return;
      }

      setFinalPrompt(filledPrompt);
      setStep(4);
      
      console.log('Form submitted successfully', { 
        fieldsFilled: Object.keys(formValues).length,
        promptLength: filledPrompt.length 
      });
      
    } catch (error) {
      handleError('form_submission', error, { 
        formValues: Object.keys(formValues),
        schemaFields: schema?.formFields?.length 
      });
    }
  };

  // Fill template with user values
  const fillTemplate = (template, values) => {
    if (!template || !values) {
      return template || '';
    }

    let filledTemplate = template;
    
    // Replace all {{variableName}} with actual values
    Object.keys(values).forEach(key => {
      const regex = new RegExp(`\\{\\{${key}\\}\\}`, 'g');
      const value = values[key] || '';
      filledTemplate = filledTemplate.replace(regex, value);
    });

    // Handle special case: {{userIntent}} - auto-populate from original userDomain if missing
    if (filledTemplate.includes('{{userIntent}}') && !values.userIntent) {
      const userIntentValue = userDomain || 'accomplish their goals';
      filledTemplate = filledTemplate.replace(/\{\{userIntent\}\}/g, userIntentValue);
      console.log('Auto-populated userIntent with:', userIntentValue);
    }

    // Log for debugging
    console.log('Template filled:', filledTemplate);
    console.log('Variables replaced:', Object.keys(values));
    
    return filledTemplate;
  };

  // Copy to clipboard functionality
  const handleCopyToClipboard = async () => {
    try {
      if (!finalPrompt || finalPrompt.trim() === '') {
        handleError('clipboard', new Error('No prompt to copy'), { finalPromptLength: finalPrompt?.length });
        return;
      }

      await navigator.clipboard.writeText(finalPrompt);
      setCopySuccess(true);
      
      console.log('Prompt copied successfully', { 
        promptLength: finalPrompt.length 
      });
      
      // Hide success message after 3 seconds
      setTimeout(() => {
        setCopySuccess(false);
      }, 3000);
    } catch (err) {
      console.error('Failed to copy to clipboard:', err);
      
      try {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = finalPrompt;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        const successful = document.execCommand('copy');
        document.body.removeChild(textArea);
        
        if (successful) {
          setCopySuccess(true);
          setTimeout(() => {
            setCopySuccess(false);
          }, 3000);
          console.log('Prompt copied using fallback method', { 
            promptLength: finalPrompt.length 
          });
        } else {
          throw new Error('Fallback copy command failed');
        }
      } catch (fallbackErr) {
        console.error('Fallback copy failed:', fallbackErr);
        handleError('clipboard', new Error('Failed to copy to clipboard. Please select and copy manually.'), { 
          originalError: err.message,
          fallbackError: fallbackErr.message,
          promptLength: finalPrompt.length 
        });
      }
    }
  };

  // Render individual form field
  const renderFormField = (field) => {
    const fieldId = field.id;
    const value = formValues[fieldId] || '';

    return (
      <div key={fieldId} className="form-field">
        <label htmlFor={fieldId} className="field-label">
          {field.question}
          {field.required && <span className="required"> *</span>}
        </label>
        
        <div className="field-input-container">
          {field.type === 'text' && (
            <input
              id={fieldId}
              type="text"
              value={value}
              onChange={(e) => handleFieldChange(fieldId, e.target.value)}
              placeholder={field.placeholder}
              className="field-input"
              required={field.required}
            />
          )}
          
          {field.type === 'textarea' && (
            <textarea
              id={fieldId}
              value={value}
              onChange={(e) => handleFieldChange(fieldId, e.target.value)}
              placeholder={field.placeholder}
              className="field-textarea"
              rows={4}
              required={field.required}
            />
          )}
          
          {field.type === 'select' && (
            <select
              id={fieldId}
              value={value}
              onChange={(e) => handleFieldChange(fieldId, e.target.value)}
              className="field-select"
              required={field.required}
            >
              <option value="">Choose an option...</option>
              {field.options.map((option, index) => (
                <option key={index} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
          )}
          
          <button
            type="button"
            onClick={() => handleUseSample(fieldId)}
            className="sample-button"
            title="Use sample text for testing"
          >
            📝 Use Sample
          </button>
        </div>
        
        {field.helpText && (
          <small className="field-help">
            {field.helpText}
          </small>
        )}
      </div>
    );
  };

  // Render landing page (Step 1)
  const renderLandingPage = () => (
    <div className="landing-page">
      <div className="container">
      <header className="header">
        <h1>The Prompt Architect</h1>
        <p className="subtitle">
          A free tool that helps you surface what you actually mean to ask. Starting with why, not what. It turns raw needs into structured prompts with roles, goals, and constraints — revealing the reasoning beneath your request.
        </p>
      </header>


        {/* INPUT FORM */}
        <div className="form-section">
          <div className="input-group">
            <label htmlFor="userDomain">
              What do you need? *
            </label>
            <textarea
              id="userDomain"
              value={userDomain}
              onChange={(e) => setUserDomain(e.target.value)}
              placeholder="e.g., I need to write wedding vows that sound like me - funny, honest, not poetic"
              rows={4}
              className="domain-input"
            />
            <small className="help-text">
              Be specific. Generic → generic template. Detailed → useful template.
            </small>
          </div>

          {/* Example hint if example was loaded */}
          {showExampleHint && (
            <div className="example-hint">
              💡 This is a <strong>format guide</strong> - edit it to match your situation, then generate
            </div>
          )}

          {/* ADDITIONAL CONTEXT FIELD - TOGGLE */}
          <div className="context-toggle-section">
            <button
              type="button"
              onClick={() => setShowContextField(!showContextField)}
              className="context-toggle-button"
            >
              <span className="context-toggle-icon">{showContextField ? '−' : '+'}</span>
              <span>Additional context (optional)</span>
            </button>

            {showContextField && (
              <div className="context-input-container">
                <div className="input-group" id="context-input-group">
                  <input
                    id="userFraming"
                    type="text"
                    value={userFraming}
                    onChange={(e) => setUserFraming(e.target.value)}
                    placeholder="e.g., I'm terrible at being emotional, I want something professional, I need it to be funny..."
                    className="framing-input"
                  />
                  <small className="help-text">
                    Any additional guidance about style, tone, or approach.
                  </small>
                </div>
              </div>
            )}
          </div>

          {error && (
            <div className="error-message">
              <div className="error-content">
                <span className="error-text">{error}</span>
                {canRetry(lastErrorType) && (
                  <div className="error-actions">
                    <button 
                      onClick={handleRetry} 
                      className="retry-button"
                      disabled={loading}
                    >
                      🔄 Try Again ({3 - retryCount} attempts left)
                    </button>
                  </div>
                )}
              </div>
            </div>
          )}

          <button
            onClick={handleGenerateTemplate}
            disabled={loading || !userDomain.trim()}
            className="generate-button"
          >
            {loading ? 'Refining my ask...' : 'Design My Prompt'}
          </button>
        </div>


        {/* DIVIDER */}
        <div className="or-divider">
          <span>or start with an example</span>
        </div>

        {/* EXAMPLES FIRST - ABOVE THE FOLD */}
        <div className="examples-section-primary">
          <p className="examples-subtitle">
            See how to describe your need (click any to load)
          </p>
          <div className="example-cards-inline">
            <button 
              className="example-card-compact"
              onClick={() => loadExample('groomsman')}
              type="button"
            >
              <span className="example-icon">💬</span>
              <span className="example-label">Groomsman Speech</span>
            </button>
            
            <button 
              className="example-card-compact"
              onClick={() => loadExample('performance')}
              type="button"
            >
              <span className="example-icon">📊</span>
              <span className="example-label">Performance Review</span>
            </button>
            
            <button 
              className="example-card-compact"
              onClick={() => loadExample('apology')}
              type="button"
            >
              <span className="example-icon">🤝</span>
              <span className="example-label">Apology Letter</span>
            </button>
            
            <button 
              className="example-card-compact"
              onClick={() => loadExample('vows')}
              type="button"
            >
              <span className="example-icon">💍</span>
              <span className="example-label">Wedding Vows</span>
            </button>
            
            <button 
              className="example-card-compact"
              onClick={() => loadExample('email')}
              type="button"
            >
              <span className="example-icon">📧</span>
              <span className="example-label">Difficult Email</span>
            </button>

            <button 
              className="example-card-compact"
              onClick={() => loadExample('explainCode')}
              type="button"
            >
              <span className="example-icon">💻</span>
              <span className="example-label">Understand Code</span>
            </button>

            <button 
              className="example-card-compact"
              onClick={() => loadExample('learnMath')}
              type="button"
            >
              <span className="example-icon">🔢</span>
              <span className="example-label">Learn Math</span>
            </button>
          </div>
        </div>

        {/* HOW IT WORKS - MOVED TO BOTTOM */}
        <div className="info-section">
          <h3>How this works:</h3>
          <ol>
            <li><strong>Describe what you need</strong> - Be specific about your situation</li>
            <li><strong>Get a custom template</strong> - Tool generates a structured prompt</li>
            <li><strong>Answer the questions</strong> - Fill in your specific details</li>
            <li><strong>Copy and use</strong> - Take the final prompt to ChatGPT, Claude, or any AI</li>
          </ol>
          <p className="info-note">
            💡 This tool creates prompts that prevent generic AI output. It's free and runs entirely in your browser.
          </p>
        </div>
      </div>
    </div>
  );

  // Render loading state (Step 2)
  const renderLoadingPage = () => (
    <div className="loading-page">
      <div className="container">
        <div className="loading-content">
          <div className="spinner"></div>
          <h2>Generating Your Custom Template</h2>
          
          {/* ROTATING TIPS */}
          <div className="loading-tip">
            <p key={currentTip} className="tip-text">
              {LOADING_TIPS[currentTip]}
            </p>
          </div>
          
          {/* PROGRESS CHECKLIST */}
          <div className="loading-details">
            <p className="complete">Identifying common patterns to avoid</p>
            <p className="complete">Extracting key variables needed</p>
            <p className="complete">Building structured template</p>
            <p className="complete">Creating personalized questions</p>
          </div>
        </div>
      </div>
    </div>
  );

  // Render form page (Step 3)
  const renderFormPage = () => {
    // Generate live preview as user types
    const livePreview = schema?.promptTemplate 
      ? fillTemplate(schema.promptTemplate, formValues)
      : '';
    
    // Calculate completion percentage
    const totalFields = schema?.formFields?.length || 1;
    const completedFields = Object.keys(formValues).filter(key => 
      formValues[key] && formValues[key].toString().trim() !== ''
    ).length;
    const completionPercentage = (completedFields / totalFields) * 100;
    
    return (
      <div className="form-page">
        <div className="container-split">
          
          {/* LEFT: FORM */}
          <div className="form-column">
            <header className="form-header">
              <h2>Customize Your Prompt</h2>
              <p>Fill in the details below to personalize your prompt template.</p>
            </header>

            {/* Dynamic form */}
            <form onSubmit={handleFormSubmit} className="dynamic-form">
              {schema?.formFields?.map(field => renderFormField(field))}

              {/* Anti-patterns section - moved to bottom */}
              {schema?.antiPatterns && schema.antiPatterns.length > 0 && (
                <div className="anti-patterns-section">
                  <h3>⚠️ What We'll Help You Avoid</h3>
                  <div className="anti-patterns-list">
                    {schema.antiPatterns.map((pattern, index) => (
                      <div key={index} className="anti-pattern-item">
                        {pattern}
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {error && (
                <div className="error-message">
                  <div className="error-content">
                    <span className="error-text">{error}</span>
                    {canRetry(lastErrorType) && (
                      <div className="error-actions">
                        <button
                          onClick={handleRetry}
                          className="retry-button"
                          disabled={loading}
                        >
                          🔄 Try Again ({3 - retryCount} attempts left)
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              )}

              <div className="form-actions">
                <button type="submit" className="generate-button">
                  Generate Final Prompt
                </button>
                <button type="button" onClick={handleStartOver} className="secondary-button">
                  Start Over
                </button>
              </div>
            </form>

            {/* Debug Console */}
            <div className="debug-console">
              <button
                type="button"
                onClick={() => setShowDebug(!showDebug)}
                className="debug-toggle"
              >
                {showDebug ? '🔽' : '🔼'} Debug Console
              </button>
              {showDebug && (
                <div className="debug-content">
                  <div className="debug-section">
                    <h4>Raw AI Output:</h4>
                    <pre className="debug-pre">{templateData?.output || 'No data'}</pre>
                  </div>
                  <div className="debug-section">
                    <h4>Parsed Schema:</h4>
                    <pre className="debug-pre">{JSON.stringify(schema, null, 2)}</pre>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* RIGHT: LIVE PREVIEW */}
          <div className="preview-column">
            <div className="preview-sticky">
              <h3>👁️ Live Preview</h3>
              <p className="preview-subtitle">Your prompt updates as you type</p>
              
              {/* Progress bar */}
              <div className="preview-progress">
                <div className="progress-bar">
                  <div 
                    className="progress-fill"
                    style={{ width: `${completionPercentage}%` }}
                  />
                </div>
                <p className="progress-text">
                  {completedFields} of {totalFields} fields completed
                </p>
              </div>

              {/* Preview content */}
              <div className="preview-content">
                <pre className="preview-text">
                  {livePreview || 'Fill in the form to see your prompt build in real-time...'}
                </pre>
              </div>

              {/* Tip */}
              <div className="preview-tip">
                <p>💡 Tip: Watch your prompt come to life as you type</p>
              </div>

              {/* Action Buttons */}
              <div className="preview-actions">
                <button
                  type="button"
                  onClick={handleAddRelevantDetail}
                  className="preview-action-button secondary"
                >
                  Add Relevant Detail
                </button>
                <button
                  type="button"
                  onClick={handleFastModeClick}
                  className="preview-action-button primary"
                >
                  Fast Mode
                </button>
              </div>
            </div>
          </div>

          {/* Fast Mode Dialog */}
          {showFastModeDialog && (
            <div className="dialog-overlay" onClick={handleFastModeCancel}>
              <div className="dialog-content" onClick={(e) => e.stopPropagation()}>
                <h3 className="dialog-title">Are you sure you want to skip?</h3>
                <p className="dialog-body">
                  The questions below help you get AI sophistication — and that's what leads to better answers.
                </p>
                <div className="dialog-actions">
                  <button
                    type="button"
                    onClick={handleFastModeConfirm}
                    className="dialog-button confirm"
                  >
                    Got it
                  </button>
                  <button
                    type="button"
                    onClick={handleFastModeCancel}
                    className="dialog-button cancel"
                  >
                    Cancel
                  </button>
                </div>
              </div>
            </div>
          )}

        </div>
      </div>
    );
  };

  // Render result page (Step 4)
  const renderResultPage = () => (
    <div className="result-page">
      <div className="container">
        <header className="result-header">
          <h2>🎉 Your Custom Prompt is Ready!</h2>
          <p>Copy the prompt below and use it with ChatGPT, Claude, or any AI assistant.</p>
        </header>

        {/* Success message */}
        {copySuccess && (
          <div className="success-message">
            ✅ Prompt copied to clipboard!
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="error-message">
            <div className="error-content">
              <span className="error-text">{error}</span>
              {canRetry(lastErrorType) && (
                <div className="error-actions">
                  <button 
                    onClick={handleRetry} 
                    className="retry-button"
                    disabled={loading}
                  >
                    🔄 Try Again ({3 - retryCount} attempts left)
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Final prompt display */}
        <div className="prompt-container">
          <div className="prompt-header">
            <h3>Your Custom Prompt</h3>
            <button 
              onClick={handleCopyToClipboard}
              className="copy-button"
              disabled={!finalPrompt}
            >
              📋 Copy to Clipboard
            </button>
          </div>
          
          <div className="prompt-content">
            <pre className="prompt-text">{finalPrompt}</pre>
          </div>
        </div>

        {/* Feedback section */}
        {!feedbackGiven && (
          <div className="feedback-section">
            <p className="feedback-question">Was this prompt helpful?</p>
            <div className="feedback-buttons">
              <button 
                onClick={() => handleFeedback('helpful')}
                className="feedback-button positive"
              >
                👍 Yes, this is helpful
              </button>
              <button 
                onClick={() => handleFeedback('not-helpful')}
                className="feedback-button negative"
              >
                👎 Needs improvement
              </button>
            </div>
          </div>
        )}

        {feedbackGiven && (
          <div className="feedback-thanks">
            {feedbackType === 'helpful' ? (
              <p>✨ Thanks! We're glad this was helpful.</p>
            ) : (
              <p>📝 Thanks for the feedback. We're constantly improving.</p>
            )}
          </div>
        )}

        {/* Action buttons */}
        <div className="result-actions">
          <button 
            onClick={handleTryPrompt}
            className="secondary-button"
            disabled={generatingExample}
          >
            {generatingExample ? '⏳ Generating Example...' : '🤖 See Example Output'}
          </button>
          <button onClick={handleStartOver} className="secondary-button">
            Create Another Prompt
          </button>
        </div>

        {/* Example output section */}
        {showExample && (
          <div className="example-output-section">
            <div className="example-output-header">
              <h3>Example Output</h3>
              <p>This is what your prompt produces when used with AI:</p>
            </div>
            {generatingExample ? (
              <div className="example-loading">
                <div className="spinner"></div>
                <p>Generating example output...</p>
              </div>
            ) : (
              <div className="example-output-content">
                <pre className="example-output-text">{exampleOutput}</pre>
                <p className="example-disclaimer">
                  Note: This is just one example. Your actual results may vary based on how you use the prompt and which AI system you use.
                </p>
              </div>
            )}
          </div>
        )}

        {/* Usage instructions */}
        <div className="usage-instructions">
          <h4>How to use this prompt:</h4>
          <ol>
            <li>Copy the prompt above</li>
            <li>Paste it into ChatGPT, Claude, or your preferred AI assistant</li>
            <li>The AI will generate content based on your specific requirements</li>
            <li>Refine the output as needed for your use case</li>
          </ol>
        </div>
      </div>
    </div>
  );

  return (
    <div className="App">
      {step === 1 && renderLandingPage()}
      {step === 2 && renderLoadingPage()}
      {step === 3 && renderFormPage()}
      {step === 4 && renderResultPage()}
    </div>
  );
}

export default App;
