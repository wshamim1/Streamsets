"""
Pipeline utilities for StreamSets Data Collector SDK 3.x
"""
import csv
from typing import List, Optional
from streamsets.sdk import DataCollector
from streamsets.sdk.sdc_models import Pipeline


def export_pipelines(sdc: DataCollector, output_file: str = 'sdc_exports.zip', 
                     pipeline_filter: Optional[str] = None) -> None:
    """
    Export pipelines from Data Collector to a zip file.
    
    Args:
        sdc: DataCollector instance
        output_file: Output zip file path
        pipeline_filter: Optional filter for pipeline titles
    """
    if pipeline_filter:
        pipelines = [p for p in sdc.pipelines if pipeline_filter in p.title]
    else:
        pipelines = sdc.pipelines.get_all()
    
    print(f"Exporting {len(pipelines)} pipeline(s)...")
    pipelines_zip_data = sdc.export_pipelines(pipelines, include_library_definitions=True)
    
    with open(output_file, 'wb') as f:
        f.write(pipelines_zip_data)
    
    print(f"Pipelines exported to {output_file}")


def get_pipeline_stages(sdc: DataCollector, pipeline_title: str, 
                        output_format: str = 'console') -> None:
    """
    Get all stages from a pipeline and output to console or CSV.
    
    Args:
        sdc: DataCollector instance
        pipeline_title: Title of the pipeline
        output_format: 'console' or 'csv'
    """
    pipeline = sdc.pipelines.get(title=pipeline_title)
    
    if output_format == 'csv':
        _export_stages_to_csv(pipeline)
    else:
        _print_stages_to_console(pipeline)


def _print_stages_to_console(pipeline: Pipeline) -> None:
    """Print stage details to console."""
    for stage in pipeline.stages:
        print(f"\n{'='*60}")
        print(f"Stage: {stage.stage_name}")
        print(f"{'='*60}")
        
        for attr in dir(stage):
            if attr.startswith("_"):
                continue
            try:
                value = getattr(stage, attr)
                print(f"{attr}: {value}")
            except (AttributeError, Exception):
                pass


def _export_stages_to_csv(pipeline: Pipeline, output_file: str = 'stages.csv') -> None:
    """Export stage details to CSV file."""
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['stage_name', 'property', 'value']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for stage in pipeline.stages:
            writer.writerow({
                'stage_name': stage.stage_name,
                'property': '',
                'value': ''
            })
            
            for attr in dir(stage):
                if attr.startswith("_"):
                    continue
                try:
                    value = getattr(stage, attr)
                    writer.writerow({
                        'stage_name': stage.stage_name,
                        'property': attr,
                        'value': str(value)
                    })
                except (AttributeError, Exception):
                    pass
    
    print(f"Stage details exported to {output_file}")

# Made with Bob
