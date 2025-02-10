import pandas as pd
import plotly.express as px
import argparse
import plotly.graph_objects as go

def main(file_path, output_file, chunk_size=10000, marker_size=2):
    # Initialize an empty list to hold chunks
    chunks = []

    # Read the data in chunks
    for chunk in pd.read_csv(file_path, delimiter='\t', chunksize=chunk_size):
        chunks.append(chunk)

    color_mapping = {
        'Germ Stem Cell': 'rgb(255, 0, 0)',    # Red rgb(0, 255, 0)
        'Spermatogenic Cell': 'rgb(0, 0, 255)',    # Blue rgb(255, 0, 0)
        'Oogenic Cell': 'rgb(0, 255, 0)'     # Green rgb(0, 0, 255)
    }
    
    color_mapping = {
    'Germ Stem Cell': 'rgb(248, 118, 109)',    # Red
    'Spermatogenic Cell': 'rgb(97, 156, 255)', # Blue
    'Oogenic Cell': 'rgb(0, 186, 56)'        # Green
    }   

    # Concatenate all chunks into a single DataFrame
    data = pd.concat(chunks, axis=0)

    data['color'] = data['class'].map(color_mapping)

    # Create a 3D scatter plot
    # Create the 3D scatter plot
    fig = go.Figure(data=[go.Scatter3d(
    x=data['UMAP_1'],
    y=data['UMAP_2'],
    z=data['UMAP_3'],
    mode='markers',
    marker=dict(
        size=10,
        color=data['color'],  # Use the mapped RGB colors
    )
    )])

    fig.update_traces(marker=dict(size=3))
    
    # Save the plot to an HTML file
    # fig.write_html(output_file)
    
    fig.update_layout(
        margin=dict(l=0, r=0, b=0, t=0),
        scene=dict(
            xaxis=dict(title='UMAP1'),
            yaxis=dict(title='UMAP2'),
            zaxis=dict(title='UMAP3'),
            aspectmode='cube'
        ),
        width=2000,  # Adjust the width as needed
        height=800   # Adjust the height as needed
    )
    
    fig.write_html("/data/c-elegans/website/public/3D.UMAP.html")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='3D Scatter Plot using Plotly')
    parser.add_argument('file_path', type=str, help='Path to the text file containing the data')
    parser.add_argument('color_column', type=str, help='Name of the column to use for color mapping')
    parser.add_argument('output_file', type=str, help='Path to save the output HTML file')
    parser.add_argument('--chunk_size', type=int, default=10000, help='Chunk size for reading the file')

    args = parser.parse_args()
    main(args.file_path, args.color_column, args.output_file, args.chunk_size)
