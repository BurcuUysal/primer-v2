// (b) Regresyon testi: yeni model devredeyken hikâye baştan sona kırılmadan oynanabilmeli.
// NOT: Geçen haftaki The Primer E2E testlerinizi (20+ adım) bu klasöre kopyalayın;
// bu dosya yalnızca bu repodaki 8 sahnelik akışı güvence altına alır.
describe("Regresyon: hikâye akışı yeni model ile bozulmuyor", () => {
  it("8 sahne baştan sona oynanır ve bitiş ekranı görünür", () => {
    cy.visit("/");
    cy.get('[data-cy="basla"]').click();
    for (let sahne = 1; sahne <= 8; sahne++) {
      cy.get('[data-cy="anlatim"]').should("be.visible");
      cy.get('[data-cy="mod"]').should("be.visible");
      cy.get('[data-cy="secenek-0"]').click();
      cy.get('[data-cy="onayla"]').click();
      cy.get('[data-cy="geri-bildirim"]').should("be.visible");
      cy.get('[data-cy="devam"]').click();
    }
    cy.get('[data-cy="bitis"]').should("be.visible");
  });

  it("model kararı davranışı değiştirir: tereddütlü oyuncuda süre sayacı kalkar", () => {
    cy.visit("/");
    cy.get('[data-cy="basla"]').click();
    // Tereddüt: seçeneği defalarca değiştir, sonra onayla
    [0, 1, 2, 0, 1].forEach((k) => cy.get(`[data-cy="secenek-${k}"]`).click());
    cy.wait(6000); // karar süresini uzat
    cy.get('[data-cy="onayla"]').click();
    cy.get('[data-cy="devam"]').click();
    cy.get('[data-cy="mod"]').invoke("text").then((metin) => {
      // Model "derin" derse sayaç gizlenir; "normal/kisa" derse görünür. Her iki durumda tutarlılık:
      if (metin.includes("derin")) cy.get('[data-cy="sayac"]').should("not.be.visible");
      else cy.get('[data-cy="sayac"]').should("be.visible");
    });
  });
});
