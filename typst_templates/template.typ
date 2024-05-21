#let cover(
  doc,
  date: datetime.today().display("[day]/[month]/[year]"),
  title: "Rapport",
  doctype: "Fiche",
  author: "Bastien Ubassy",
  source: none,
  cover_img: none,
  cover_description: "Image libre de droit",
) = {
  set text(lang: "fr")
  set page("a4")
  let page_header = smallcaps(title)
  

  place(
    image("logos.png"),
    dx: 0cm,
    dy: -1cm,
  )
  align(
    center + horizon,
    par(
      justify: false,
      text(size: 12pt, weight: "semibold", date)
    )
  )
  line(length: 100%)
  align(
    center + horizon,
    par(
      leading: 1cm,
      justify: false,
      text(size: 24pt, weight: "bold", title)
    ),
  )
  align(
    center + horizon,
    par(
      leading: 1cm,
      justify: false,
      text(size: 16pt, weight: "bold", doctype)
    ),
  )
  line(length: 100%)
  align(
    center + horizon,
    par(
      leading: 1cm,
      justify: false,
      if author != "Bastien Ubassy" {
        text(size: 16pt, weight: "semibold", "Auteurs : " + author)
      } else {
      text(size: 16pt, weight: "semibold", "Auteur : " + author)
      }
    ),
  )
  if source != none {
    align(
      center + horizon,
      par(
        leading: 1cm,
        justify: false,
        text(size: 16pt, weight: "semibold", "Professeur : " + source)
      ),
    )
  }
  if cover_img != none {
    align(
      center + horizon,
      figure(
        image(
          cover_img,
          height: 10cm,
        ),
        caption: cover_description
      )
    )
  }

  counter(page).update(0)
  set page(
    "a4",
    header-ascent: 25%,
    footer: [
      #place(
        left,
        dx: -1cm,
        image(
          "footer.png",
          height: 1cm)
      )
      #place(
        right,
        dx: 1.55cm,
        dy: 0.58cm,
        text(weight: "bold", counter(page).display())
      )
    ],
    header: [
      #v(5cm)
      #page_header
      #h(1fr)
      #if type(date) == datetime [
        #date.display("[day]/[month]/[year]")
      ] else [
        #date
      ]
      #line(length: 100%)
    ]
  )

  pagebreak()

  outline(
    title: "Table des matières",
    indent: 0.5cm,
    depth: 4
  )  

  set par(
    first-line-indent: .5cm,
    leading: 0.25cm,
    justify: true,
  )

  show heading: it =>  {
    it
    par()[#text(size:0em)[#h(0.0em)]]
  }

  show list: it =>  {
    v(.1cm)
    it
    par()[#text(size:0em)[#h(0.0em)]]
  }

  show figure: it =>  {
    it
    par()[#text(size:0em)[#h(0.0em)]]
  }

  show grid: it =>  {
    it
    par()[#text(size:0em)[#h(0.0em)]]
  }

  set list(
    indent: .8cm,
  )

  pagebreak()

  doc

  pagebreak()

  set par(
    first-line-indent: 0cm,
    leading: 0.25cm,
    justify: true,
  )

  outline(
    title: "Table des figures",
    target: figure.where(kind: image),
    depth: 4
  )
}

#let tableau(content, caption: none) = {
  figure(caption: caption, kind: "table", supplement: "Tableau", content)
}

#let sc(content) = {
  smallcaps(content)
}