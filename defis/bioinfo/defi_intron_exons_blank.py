import time
from collections import deque
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.text import Text


#MICRO - DICO
CODON_TABLE = {
    "AUG": "START",
    "AAA": "LYS",
    "AAG": "LYS",
    "GGU": "GLY",
    "GGC": "GLY",
    "GGA": "GLY",
    "GGG": "GLY",
    "CCC": "PRO",
    "CCU": "PRO",
    "CCA": "PRO",
    "UUU": "PHE",
    "UUC": "PHE",
    "UAA": "STOP",
    "UAG": "STOP",
    "UGA": "STOP",
}


# DECODEUR (VOUS DEVEZ CODER LA LOGIQUE METIER SANS FAIRE DE RETOURS EN ARRIÈRE)
class SplicingDecoder:
    """
    Do it ;)
    """

    def __init__(self):
        self.introns_found = []
        self.genes_found = []
        self.mature_mrna = ""
        self._intron_active = False
        self._intron_buffer = ""
        self._pending_g = False
        self._pending_a = False
        self._codon_buffer = []
        self._in_gene = False
        self._current_gene = []

    def _is_valid_base(self, base: str) -> bool:
        return base in ("A", "U", "G", "C")

    def _append_exon_base(self, base: str, events: list) -> None:
        self.mature_mrna += base
        self._codon_buffer.append(base)
        if len(self._codon_buffer) < 3:
            return

        codon = "".join(self._codon_buffer)
        self._codon_buffer.clear()

        token = CODON_TABLE.get(codon, "UNKNOWN")
        events.append(("CODON", codon, token))

        if token == "START":
            self._in_gene = True
            self._current_gene = ["START"]
            events.append(("START",))
        elif token == "STOP":
            if self._in_gene:
                self._current_gene.append("STOP")
                self.genes_found.append(list(self._current_gene))
                events.append(("STOP", list(self._current_gene)))
                self._current_gene = []
                self._in_gene = False
        else:
            if self._in_gene:
                self._current_gene.append(token)

    def process_base(self, base):
        events = []

        if self._intron_active:
            if self._pending_a:
                if base == "G":
                    self._intron_buffer += "AG"
                    self.introns_found.append(self._intron_buffer)
                    events.append(("INTRON_END", self._intron_buffer))
                    self._intron_buffer = ""
                    self._intron_active = False
                    self._pending_a = False
                    return events

                self._intron_buffer += "A"
                self._pending_a = False

            if base == "A":
                self._pending_a = True
                return events

            self._intron_buffer += base
            return events

        if self._pending_g:
            if base == "U":
                self._intron_active = True
                self._intron_buffer = "GU"
                self._pending_g = False
                events.append(("INTRON_START",))
                return events

            self._append_exon_base("G", events)
            self._pending_g = False

        if base == "G":
            self._pending_g = True
            return events

        if self._is_valid_base(base):
            self._append_exon_base(base, events)

        return events

    def get_mature_mrna(self):
        return self.mature_mrna

    def get_stats(self):
        return {
            "introns": len(self.introns_found),
            "genes": len(self.genes_found),
        }


# AFFICHAGE (ne pas le changer!!!!!!!!!!!!)
def style_base(b: str) -> str:
    if b in ("G", "C"):
        return "green"
    if b in ("A", "U"):
        return "yellow"
    return "bold red"


def format_genome_tape(genome_tape) -> Text:
    t = Text()
    for i, b in enumerate(genome_tape):
        if i > 0:
            t.append(" ")
        t.append(b, style=style_base(b))
    return t


def format_mrna(mrna: str) -> Text:
    if not mrna:
        return Text("—", style="dim")
    return Text(mrna, style="cyan")


def format_stats(stats: dict) -> Text:
    t = Text()
    t.append("Introns: ", style="dim")
    t.append(str(stats["introns"]), style="magenta")
    t.append("\nGènes: ", style="dim")
    t.append(str(stats["genes"]), style="yellow")
    return t


def format_event(event) -> str:
    t = event[0]

    if t == "INTRON_START":
        return "[bold magenta]INTRON_START[/bold magenta]"

    if t == "INTRON_END":
        intron = event[1]
        return f"[bold magenta]INTRON_END[/bold magenta] [dim](len={len(intron)})[/dim]"

    if t == "CODON":
        codon, token = event[1], event[2]
        if token == "START":
            return f"[bold green]{codon} = START[/bold green]"
        if token == "STOP":
            return f"[bold red]{codon} = STOP[/bold red]"
        if token == "UNKNOWN":
            return f"[bold yellow]{codon} = UNKNOWN[/bold yellow]"
        return f"[cyan]{codon} = {token}[/cyan]"

    if t == "START":
        return "[bold green]START[/bold green]"

    if t == "STOP":
        gene = event[1]
        return f"[bold red]STOP[/bold red] [dim](gene_len={len(gene)})[/dim]"

    return f"[dim]{event}[/dim]"


def render_table(genome_tape, event_log, mrna, stats) -> Table:
    table = Table(
        title="[bold bright_blue]Epissage Introns / Exons[/bold bright_blue]",
        show_lines=True,
        border_style="bright_blue",
        header_style="bold white",
    )

    table.add_column("ARN entrant", width=42, style="white", overflow="fold")
    table.add_column("Événements", width=46, style="white", overflow="fold")
    table.add_column("ARN mature", width=28, style="white", overflow="fold")
    table.add_column("Stats", width=12, style="white", overflow="fold")

    seq_text = format_genome_tape(genome_tape)
    events_text = "\n".join(event_log) if event_log else "[dim]—[/dim]"
    mrna_text = format_mrna(mrna)
    stats_text = format_stats(stats)

    table.add_row(seq_text, events_text, mrna_text, stats_text)
    return table


#prog pour run l'affichage console (TESTEZ LE DÈS LE DÉPART, vous aurez au moins avoir un apercu de L'input streaming)
def run(sequence: str, speed_sec: float = 0.20):
    console = Console()
    decoder = SplicingDecoder()

    genome_tape = []
    event_log = deque(maxlen=10)

    with Live(console=console, refresh_per_second=12) as live:
        for base in sequence:
            genome_tape.append(base)

            events = decoder.process_base(base)
            for ev in events:
                event_log.append(format_event(ev))

            table = render_table(
                genome_tape=genome_tape,
                event_log=list(event_log),
                mrna=decoder.get_mature_mrna(),
                stats=decoder.get_stats(),
            )
            live.update(table)
            time.sleep(speed_sec)


if __name__ == "__main__":
    seq1 = "AUGAAAGUxxxxAGGGUCCCUAA"
    seq2 = "AUGAAAGUxxxAGGGUGUyyyAGCCCUAA"

    run(seq1, speed_sec=0.15) #vous etes libres de changer la vitesse pour gagner du temps ;)
    time.sleep(0.6)
    run(seq2, speed_sec=0.15)
