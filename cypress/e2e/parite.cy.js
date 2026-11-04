// (a) Diferansiyel test: uygulamadaki ONNX çıkarımı (onnxruntime-web) ile
// Python Oracle (tests/parite.py -> tests/parite.json) aynı girdilere < 1e-4 fark vermeli.
const TOL = 1e-4;

describe("Diferansiyel test (parite): uygulama vs Python Oracle", () => {
  it(`5 referans girdide fark < ${TOL}`, () => {
    cy.readFile("tests/parite.json").then((referanslar) => {
      expect(referanslar).to.have.length(5);
      referanslar.forEach((ref, n) => {
        cy.visit("/?test=1");
        cy.get('[data-cy="in-seviye"]'); // model yüklenince panel çizilir
        Object.entries(ref.girdi).forEach(([ozellik, deger]) => {
          cy.get(`[data-cy="in-${ozellik}"]`).clear().type(String(deger));
        });
        cy.get('[data-cy="hesapla"]').click();
        cy.get('[data-cy="p"]')
          .should(($p) => expect($p.text()).to.not.equal("—"))
          .then(($p) => {
            const p = parseFloat($p.text());
            const fark = Math.abs(p - ref.p);
            cy.log(`girdi ${n}: uygulama=${p} oracle=${ref.p} fark=${fark}`);
            expect(fark, `girdi ${n} farkı`).to.be.lessThan(TOL);
          });
      });
    });
  });
});
