import click
from kobo_doccano import Kobo2Doccano


@click.command()
@click.option(
    '--doccano-project-id',
    required=True
)
@click.option(
    '--doccano-task-type',
    required=True
)
@click.option(
    '--doccano-format', required=True,
    type=click.Choice([
        "AudioFile",
    ])
)
@click.option(
    '--kobo-form-id',
    required=True
)
@click.option(
    '--kobo-audio-quality',
    required=True
)
def main(
    doccano_project_id,
    doccano_task_type,
    doccano_format,
    kobo_form_id,
    kobo_audio_quality
):
    k2d = Kobo2Doccano(
        doccano_project_id=doccano_project_id,
        doccano_format=doccano_format,
    )
    profile = k2d.doccano.get_profile()
    k2d.upload_audio_from_doccano(
        kobo_form_id, kobo_audio_quality, doccano_task_type)


if __name__ == "__main__":
    main()

# Example:
# --------

# python3 upload_kobo2doccano.py --doccano-project-id = 3 --doccano-task-type=Speech2text --doccano-format=AudioFile --kobo-form-id=a7mtb2bg6X6AaZqVdPmjJt --kobo-audio-quality=download_url
