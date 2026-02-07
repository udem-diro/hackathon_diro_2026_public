import time
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.columns import Columns
from rich.layout import Layout
from rich.table import Table


CODON_TABLE = {
    "AUG": "START",
    "ACG": "START",
    "AAA": "LYS",
    "AAC": "ASN",
    "AAU": "ASN",
    "GGU": "GLY",
    "GGC": "GLY",
    "GGA": "GLY",
    "GGG": "GLY",
    "UUU": "PHE",
    "UUC": "PHE",
    "CCC": "PRO",
    "CCU": "PRO",
    "UAA": "STOP",
    "UAG": "STOP",
    "UGA": "STOP",
}


class FrameDecoder:
    def __init__(self, frame_id: int):
     pass

    def process_base(self, base: str):

        self.base_count += 1
        return []

    def get_score(self):
        return 0

    def get_best_gene(self):
        return None


class MultiFrameDecoder:
    def __init__(self):
        self.frames = [
            #(...)
        ]

    def process_base(self, base: str):
        """
        Distribue la base à tous les frames
        """
        for frame in self.frames:
            frame.process_base(base)

    def get_best_frame(self):
        """
        Retourne l'indice du frame considéré comme le meilleur selon vous ;)
        """
        return 0


# AFFICHAGE CONSOLE - NE LE CHANGEZ PAS

def render_frame_panel(frame: FrameDecoder, is_best: bool = False):
    border = "green" if is_best else "blue"
    title = f"Frame {frame.frame_id}"

    content = ""
    content += f"Bases lues: {frame.base_count}\n"
    content += f"Codons: {frame.codon_count}\n"
    content += f"Gènes: {len(frame.all_genes)}\n"
    content += f"Score: {frame.get_score()}"

    return Panel(content, title=title, border_style=border)


def render_genome_panel(genome_tape):
    display = " ".join(genome_tape)
    return Panel(display, title="Flux ARN", border_style="cyan")


def render_comparison_table(frames):
    table = Table(title="Comparaison des frames")

    table.add_column("Frame")
    table.add_column("Bases")
    table.add_column("Codons")
    table.add_column("Gènes")
    table.add_column("Score")

    for frame in frames:
        table.add_row(
            str(frame.frame_id),
            str(frame.base_count),
            str(frame.codon_count),
            str(len(frame.all_genes)),
            str(frame.get_score()),
        )

    return table


####################################################
if __name__ == "__main__":
    console = Console()

    genome = (
        "GCUAAGGCCUUGAACCGGAUACCCGUGAAGUUAACCGGGUAACCUAGGCUAAC"
        "GGAUUGCCAAUGGCCUAA"
    )

    decoder = MultiFrameDecoder()
    genome_tape = []

    console.print("\n[MULTI-FRAME GENOME DECODER]\n")

    with Live(console=console, refresh_per_second=6) as live:
        for base in genome:
            genome_tape.append(base)
            decoder.process_base(base)

            best_frame = decoder.get_best_frame()

            genome_panel = render_genome_panel(genome_tape)

            frame_panels = [
                render_frame_panel(frame, is_best=(i == best_frame))
                for i, frame in enumerate(decoder.frames)
            ]

            layout = Layout()
            layout.split_column(
                Layout(genome_panel, size=5),
                Layout(Columns(frame_panels, equal=True), size=10),
            )

            live.update(layout)
            time.sleep(0.25)

    console.print("\nAnalyse terminée\n")
    console.print(render_comparison_table(decoder.frames))
