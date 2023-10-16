import matplotlib.pyplot as plt

from db.db_utils import close_database, get_paper_work_status_count, get_paper_count, get_total_paper_count, \
    open_database


def get_bar_values(args):
    conn, cur = open_database(args.db_host, args.db_username, args.db_password)
    total_papers = get_total_paper_count(conn, cur)
    abstract_date_added_papers = get_paper_work_status_count(conn, cur, 'abstract_added', True)
    text_extracted_papers = get_paper_count(conn, cur, 1)
    section_devided_papers = get_paper_work_status_count(conn, cur, 'section_extracted', True)

    close_database(conn, cur)
    return total_papers, abstract_date_added_papers, text_extracted_papers, section_devided_papers


def show_chart(args):
    # Set the labels and values
    labels = ['Total', 'Abstract', 'Text', 'Section']
    values = list(get_bar_values(args))

    # Set the color scheme
    colors = ['#ff7f0e', '#1f77b4', '#2ca02c', '#a103fc']

    # Create the bar chart
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors)

    # Add the value of each bar
    for i, v in enumerate(values):
        ax.text(i, v + 2, str(v), ha='center')

    # Add labels and title
    plt.xlabel('Status', fontsize=14, fontweight='bold')
    plt.ylabel('Papers', fontsize=14, fontweight='bold')
    plt.title('Papers DB Status', fontsize=16, fontweight='bold')

    # Customize the tick labels
    ax.tick_params(axis='both', which='major', labelsize=12)

    # Remove the top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Show the plot
    plt.show()
