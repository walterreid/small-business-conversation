# Template Generation Scripts

This directory contains scripts for generating templates from `meta-prompt-system.md`.

## Files

- **`generate_templates.py`** - Main script to generate templates for all categories
- **`template_parser.py`** - Parses meta-prompt output into structured JSON
- **`smb_data_loader.py`** - Loads SMB insights (with graceful fallback)

## Usage

### Generate Templates (Mock Mode - Testing)

```bash
cd backend
python3 scripts/generate_templates.py --mock
```

This generates mock templates for all categories without calling OpenAI API.

### Generate Templates (Real - All Categories)

```bash
cd backend
source venv/bin/activate
python3 scripts/generate_templates.py
```

**Cost**: ~$0.30 total for all 5 categories (one-time)

### Generate Template (Real - Single Category)

```bash
cd backend
source venv/bin/activate
python3 scripts/generate_templates.py --category restaurant
```

**Cost**: ~$0.06 per category

## Output

Templates are saved to `backend/prompts/generated_templates/`:
- `restaurant.json`
- `retail_store.json`
- `professional_services.json`
- `ecommerce.json`
- `local_services.json`

## Template Structure

Each template includes:
- `category` - Business category name
- `opening_dialog` - Chat opening message
- `anti_patterns` - Common patterns to avoid
- `prompt_template` - Template with {{variables}} for chat context
- `questions` - Form questions for sidebar
- `smb_insights` - Small business marketing insights

## Requirements

- OpenAI API key in `.env` file
- Python dependencies installed (`pip install -r requirements.txt`)

## Notes

- Templates are generated once (or when categories change)
- Mock mode is available for testing without API calls
- Script includes retry logic and error handling
- Logs are written to `template_generation.log`

