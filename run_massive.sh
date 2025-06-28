#!/bin/bash

# Massive Scale Company Generation Script
# Usage: ./run_massive.sh [num_batches] [industry_groups]

NUM_BATCHES=${1:-8}  # Default to 8 parallel batches
INDUSTRY_MODE=${2:-"all"}  # Default to all industries

echo "🚀 Starting massive scale company generation..."
echo "📊 Running $NUM_BATCHES parallel batches"
echo "🏭 Mode: $INDUSTRY_MODE"

# Create logs directory
mkdir -p logs

# Define industry groups for focused processing
declare -A INDUSTRY_GROUPS
INDUSTRY_GROUPS[1]="Finance,Investment & Private Markets"
INDUSTRY_GROUPS[2]="Technology,Technology & Innovation"
INDUSTRY_GROUPS[3]="Strategy & Management Consulting,Professional Services"
INDUSTRY_GROUPS[4]="Healthcare,Legal Services"
INDUSTRY_GROUPS[5]="Policy & International Affairs,Media & Publishing"
INDUSTRY_GROUPS[6]="Research & Academia,Emerging Industries"
INDUSTRY_GROUPS[7]="Government & Public Sector,Non-Profit & NGO"
INDUSTRY_GROUPS[8]="Arts & Culture,High-End Retail & Luxury"

# Function to run a single batch
run_batch() {
    local batch_num=$1
    local industries=$2
    
    echo "🔄 Starting batch $batch_num..."
    
    if [ "$INDUSTRY_MODE" == "all" ]; then
        # Run all industries for this batch
        BATCH_NUM=$batch_num python main.py > logs/batch_${batch_num}.log 2>&1
    else
        # Run specific industry group
        BATCH_NUM=$batch_num python main.py batch "$industries" > logs/batch_${batch_num}.log 2>&1
    fi
    
    echo "✅ Batch $batch_num completed!"
}

# Start all batches in parallel
pids=()

for ((i=1; i<=NUM_BATCHES; i++)); do
    if [ "$INDUSTRY_MODE" == "focused" ] && [ ${INDUSTRY_GROUPS[$i]+_} ]; then
        # Use predefined industry groups
        run_batch $i "${INDUSTRY_GROUPS[$i]}" &
    else
        # Run all industries with different batch numbers
        run_batch $i "all" &
    fi
    
    pids+=($!)
    echo "🏃 Started batch $i (PID: $!)"
    
    # Small delay to avoid overwhelming the system
    sleep 2
done

echo ""
echo "🏁 All $NUM_BATCHES batches started!"
echo "📂 Logs available in: logs/batch_*.log"
echo "📊 Monitor progress with: tail -f logs/batch_*.log"
echo ""

# Function to show progress
show_progress() {
    echo "📊 Current Progress:"
    for ((i=1; i<=NUM_BATCHES; i++)); do
        if [ -f "data/companies_batch${i}.db" ]; then
            count=$(sqlite3 data/companies_batch${i}.db "SELECT COUNT(*) FROM companies;" 2>/dev/null || echo "0")
            role_count=$(sqlite3 data/companies_batch${i}.db "SELECT COUNT(*) FROM roles;" 2>/dev/null || echo "0")
            echo "  Batch $i: $count companies, $role_count roles"
        else
            echo "  Batch $i: Starting..."
        fi
    done
    echo ""
}

# Monitor progress
echo "🔍 Monitoring progress (Ctrl+C to stop monitoring, processes will continue)..."
while true; do
    sleep 30
    show_progress
    
    # Check if all processes are still running
    running=0
    for pid in "${pids[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            running=$((running + 1))
        fi
    done
    
    if [ $running -eq 0 ]; then
        echo "🎉 All batches completed!"
        break
    fi
    
    echo "⏳ $running batches still running..."
done

# Final summary
echo ""
echo "🎯 Final Results:"
total_companies=0
total_roles=0

for ((i=1; i<=NUM_BATCHES; i++)); do
    if [ -f "data/companies_batch${i}.db" ]; then
        count=$(sqlite3 data/companies_batch${i}.db "SELECT COUNT(*) FROM companies;" 2>/dev/null || echo "0")
        role_count=$(sqlite3 data/companies_batch${i}.db "SELECT COUNT(*) FROM roles;" 2>/dev/null || echo "0")
        echo "  Batch $i: $count companies, $role_count roles"
        total_companies=$((total_companies + count))
        total_roles=$((total_roles + role_count))
    fi
done

echo ""
echo "🏆 TOTAL: $total_companies companies, $total_roles roles"
echo "🗂️  Data stored in: data/companies_batch*.db"
echo "🔍 Pinecone namespaces: dense-companies-claude-v8-batch*"
echo ""

if [ $total_companies -ge 100000 ]; then
    echo "🎉 SUCCESS: Reached 100K+ companies target!"
else
    needed=$((100000 - total_companies))
    echo "📈 Need $needed more companies to reach 100K target"
    echo "💡 Run again with more batches: ./run_massive.sh 12"
fi