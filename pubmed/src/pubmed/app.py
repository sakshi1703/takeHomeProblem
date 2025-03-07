import argparse
import csv
from fetchPaper import fetch_paper_ids, fetch_paper_details, filter_non_academic_authors

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed.")
    parser.add_argument("query", type=str, help="Search query for PubMed")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()
    
    if args.debug:
        print(f"Fetching papers for query: {args.query}")
    
    paper_ids = fetch_paper_ids(args.query)
    if args.debug:
        print(f"Found {len(paper_ids)} papers.")

    papers = fetch_paper_details(paper_ids)
    papers = filter_non_academic_authors(papers)

    if args.file:
        with open(args.file, "w", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=papers[0].keys())
            writer.writeheader()
            writer.writerows(papers)
        print(f"Results saved to {args.file}")
    else:
        for paper in papers:
            print(paper)

if __name__ == "__main__":
    main()
