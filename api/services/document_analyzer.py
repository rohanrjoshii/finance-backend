import csv
import io
import re

def generate_insights(income: float, expense_abs: float) -> tuple[str, str]:
    total_flow = income + expense_abs
    if total_flow == 0: total_flow = 1
    income_pct = min((income / total_flow) * 100, 100)
    expense_pct = min((expense_abs / total_flow) * 100, 100)
    
    advice = "#### 💡 Strategic Recommendations for Improvement\n\n"
    if income == 0 and expense_abs == 0:
        advice += "*   **Data Insufficient**: No significant cash flow patterns were detected to synthesize advice.\n"
    elif expense_abs > income:
        deficit = expense_abs - income
        advice += f"*   **🚨 Critical Deficit Detected**: Your expenditures currently exceed your income by **₹{deficit:,.2f}**. You are burning cash.\n"
        advice += "*   **Immediate Action Required**: Freeze all non-essential categorical spending immediately. Aim to cut discretionary outflows by at least 25% this month to serialize your cash flow.\n"
        advice += f"*   **Target Goal**: Reduce total monthly expenses to under **₹{(income * 0.8):,.2f}** to establish a healthy baseline.\n"
    else:
        net = income - expense_abs
        savings_rate = (net / income) * 100 if income else 0
        if savings_rate < 20:
            advice += f"*   **⚠️ Caution - Low Savings Rate**: You are retaining only **{savings_rate:.1f}%** of your gross capital.\n"
            advice += "*   **Optimization Strategy**: Standard financial architecture (the 50/30/20 rule) recommends preserving at least 20%. Look for recurring utility or subscription leaks to squeeze out more efficiency.\n"
        else:
            advice += f"*   **✅ Excellent Health**: You are retaining a robust **{savings_rate:.1f}%** margin on your cash flow!\n"
            advice += "*   **Next Steps**: Consider sweeping your surplus cash overflow into high-yield automated compounding vaults or index equity to beat inflation drag.\n"

    bar_chart_html = f"""
<div class="my-8 p-6 bg-slate-900/50 rounded-2xl border border-slate-700/50 shadow-inner">
    <h4 class="text-sm font-bold text-slate-300 uppercase tracking-widest mb-6 text-center">Cash Flow Distribution (Graph)</h4>
    <div class="flex flex-col gap-6">
        <div>
            <div class="flex justify-between text-xs font-bold text-slate-400 mb-2 uppercase">
                <span>Gross Income</span>
                <span class="text-emerald-400">₹{income:,.0f}</span>
            </div>
            <div class="w-full bg-slate-800 rounded-full h-4 overflow-hidden border border-slate-700 shadow-inner group">
                <div class="bg-gradient-to-r from-emerald-600 to-emerald-400 h-full rounded-full transition-all duration-1000 origin-left" style="width: {income_pct}%"></div>
            </div>
        </div>
        <div>
            <div class="flex justify-between text-xs font-bold text-slate-400 mb-2 uppercase">
                <span>Expenditures</span>
                <span class="text-rose-400">₹{expense_abs:,.0f}</span>
            </div>
            <div class="w-full bg-slate-800 rounded-full h-4 overflow-hidden border border-slate-700 shadow-inner group">
                <div class="bg-gradient-to-r from-rose-600 to-rose-400 h-full rounded-full transition-all duration-1000 origin-left" style="width: {expense_pct}%"></div>
            </div>
        </div>
    </div>
</div>
"""
    return advice, bar_chart_html

def parse_csv(file_bytes: bytes) -> str:
    text = file_bytes.decode('utf-8', errors='replace')
    reader = csv.reader(io.StringIO(text))
    rows = list(reader)
    if not rows: return "### Analysis Error\nCSV file is empty."
        
    data_rows = rows[1:] if len(rows) > 1 else rows
    total_records = len(data_rows)
    amounts = []
    
    for row in data_rows:
        for col in row:
            clean_col = col.replace(',', '').replace('₹', '').replace('$', '').strip()
            try:
                val = float(clean_col)
                if val != 0 and str(val) != clean_col: amounts.append(val); break
                elif val != 0 and len(clean_col) < 8: amounts.append(val); break
            except ValueError: continue
                
    income = sum(a for a in amounts if a > 0)
    expense = sum(a for a in amounts if a < 0)
    expense_abs = abs(expense)
    net = income + expense
    
    if not amounts: amounts = [0]
    
    advice, chart = generate_insights(income, expense_abs)
        
    return f"""### Financial Report Analysis (CSV)
**Total Records Processed**: {total_records} lines.
{chart}
#### Key Metrics Extracted
*   **Total Gross Income**: ₹{income:,.2f}
*   **Total Expenditures**: ₹{expense_abs:,.2f}
*   **Net Cash Flow**: ₹{net:,.2f}
*   **Largest Single Transaction**: ₹{max(amounts):,.2f}

{advice}

> [!NOTE]
> This analysis was generated locally using deterministic rule-based algorithms. No AI models were used.
"""

def parse_pdf(file_bytes: bytes) -> str:
    try:
        import pypdf
    except ImportError:
        return "### Error\nPyPDF is not installed on the server."
        
    try:
        reader = pypdf.PdfReader(io.BytesIO(file_bytes))
        text = ""
        for page in reader.pages: text += page.extract_text() + "\n"
            
        currency_pattern = r'[\$₹]\s?\d+(?:,\d{3})*(?:\.\d{2})?'
        amounts_found = re.findall(currency_pattern, text)
        
        numeric_amounts = []
        for a in amounts_found:
            clean = a.replace(',', '').replace('₹', '').replace('$', '').strip()
            try: numeric_amounts.append(float(clean))
            except: pass
                
        if not numeric_amounts: numeric_amounts = [0]
        
        numeric_amounts.sort(reverse=True)
        split_idx = max(1, len(numeric_amounts) // 4)
        income = sum(numeric_amounts[:split_idx])
        expense_abs = sum(numeric_amounts[split_idx:])
        
        advice, chart = generate_insights(income, expense_abs)
        
        return f"""### Financial Report Analysis (PDF)
**Pages Scanned**: {len(reader.pages)} page(s).
{chart}
#### Extracted Pattern Metrics
*   **Unique Financial Entities Detected**: {len(amounts_found)} distinct instances.
*   **Estimated Primary Capital Inflow**: ₹{income:,.2f}
*   **Estimated Total Disbursements**: ₹{expense_abs:,.2f}

{advice}

> [!NOTE]
> This report was scraped sequentially utilizing mathematical string-matching and sorting matrices directly on the PDF byte-stream. No AI models were used.
"""
    except Exception as e:
        return f"### PDF Parsing Error\nCould not extract structure: {str(e)}"

def analyze_document_rule_based(file_bytes: bytes, mime_type: str, filename: str) -> str:
    if "csv" in mime_type.lower() or filename.lower().endswith('.csv'):
        return parse_csv(file_bytes)
    elif "pdf" in mime_type.lower() or filename.lower().endswith('.pdf'):
        return parse_pdf(file_bytes)
    return "### Evaluation Failed\nUnsupported format."
