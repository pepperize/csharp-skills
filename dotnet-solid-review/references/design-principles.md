# Software Design Principles

Use these principles as review heuristics. Start from the requested behavior and the concrete
change risk, then select only the principles that help explain a material finding. Never enumerate
the catalog merely to show that it was considered. When principles pull in different directions,
prefer the smallest maintainable design for the evidence available and explain the trade-off.

The headings below are the canonical names to use in findings. A finding should name the
principle, point to affected code, explain the consequence, and suggest the smallest practical
improvement. A review may conclude that no relevant principle violation was found.

## Principles

### DRY — Don’t Repeat Yourself

**Intent:** Keep each piece of knowledge, business rule, mapping, or protocol decision in one
authoritative place.

**Review signals:** Look for the same rule changing in multiple locations, copied calculations,
duplicated mappings, or parallel branches that must stay synchronized.

**Typical violation:** Two checkout paths independently calculate the same discount rule.

**Do not apply mechanically:** Similar-looking code can represent different knowledge. Wait until
the shared concept and likely change axis are clear; a premature abstraction can couple unrelated
behavior.

**Negative example**

```csharp
decimal PriceWeb(Order order) => order.Total >= 100 ? order.Total * 0.9m : order.Total;
decimal PriceStore(Order order) => order.Total >= 100 ? order.Total * 0.9m : order.Total;
```

The discount policy is duplicated, so a threshold change can make the channels disagree.

**Positive example**

```csharp
decimal ApplyVolumeDiscount(decimal total) => total >= 100 ? total * 0.9m : total;

decimal PriceWeb(Order order) => ApplyVolumeDiscount(order.Total);
decimal PriceStore(Order order) => ApplyVolumeDiscount(order.Total);
```

The named policy owns the business knowledge while the channel operations remain distinct.

### KISS — Keep it simple, stupid

**Intent:** Choose the simplest design that clearly satisfies current behavior and constraints.

**Review signals:** Look for indirection with no payoff, meta-programming for a fixed case, deeply
nested control flow, excessive configuration, or patterns that obscure a direct solution.

**Typical violation:** A registry, factory, and strategy hierarchy selects between two stable
format strings.

**Do not apply mechanically:** Simple does not mean compressed or naive. Extra structure is useful
when it makes real complexity, safety, or variation easier to understand.

**Negative example**

```csharp
var formatter = formatterFactory.Create(formatterRegistry.Resolve("receipt"));
return formatter.Format(order);
```

The selection machinery hides a single fixed operation.

**Positive example**

```csharp
return receiptFormatter.Format(order);
```

The dependency and operation are visible without speculative machinery.

### FCoI — Favour Composition over Inheritance

**Intent:** Reuse and vary behavior by assembling focused collaborators when an `is-a`
relationship and substitutable contract are absent.

**Review signals:** Look for subclasses inheriting state or operations they do not need, overrides
used only to disable base behavior, fragile protected hooks, or inheritance chosen only for code
reuse.

**Typical violation:** An export service inherits a report class solely to reuse CSV formatting.

**Do not apply mechanically:** Keep inheritance when the subtype genuinely satisfies the base
contract, the hierarchy expresses the domain, or a framework requires it.

**Negative example**

```csharp
class Report { protected string ToCsv() => "..."; public virtual void Print() { } }
class ReportExporter : Report { public override void Print() => throw new NotSupportedException(); }
```

`ReportExporter` is not a usable `Report`; inheritance exposes an invalid operation to gain a
helper.

**Positive example**

```csharp
sealed class ReportExporter(CsvFormatter formatter)
{
    public string Export(Report report) => formatter.Format(report);
}
```

Composition supplies only the behavior the exporter needs.

### IOSP — Integration Operation Segregation Principle

**Intent:** Separate coordination from logic: an integration composes calls to project functions,
while an operation performs logic without depending on other project functions.

**Review signals:** Look for orchestration methods that interleave collaborator calls with loops,
branching, calculations, or transformations, making the decision logic hard to see and test.

**Typical violation:** A method loads orders, calculates late fees inline, and saves each result.

**Do not apply mechanically:** Do not explode a trivial readable method into tiny functions or add
injection solely for formal purity. Apply IOSP where separating meaningful logic improves
comprehension, testing, or changeability.

**Negative example**

```csharp
async Task CloseAsync(Guid id)
{
    var order = await repository.GetAsync(id);
    var fee = order.DaysLate > 5 ? order.Total * 0.1m : 0m;
    await repository.SaveAsync(order.Close(fee));
}
```

The method mixes project-level integration with fee policy.

**Positive example**

```csharp
async Task CloseAsync(Guid id)
{
    var order = await repository.GetAsync(id);
    await repository.SaveAsync(order.Close(CalculateLateFee(order)));
}

decimal CalculateLateFee(Order order) =>
    order.DaysLate > 5 ? order.Total * 0.1m : 0m;
```

The integration coordinates; the operation contains the independently testable decision.

### Single Level of Abstraction

**Intent:** Keep statements within a method or module at one conceptual level so its story can be
read without jumping between policy and implementation detail.

**Review signals:** Look for high-level workflow steps mixed with parsing, SQL, byte handling,
framework plumbing, or dense local calculations.

**Typical violation:** A checkout workflow names business steps but constructs HTTP content and
manipulates headers inline.

**Do not apply mechanically:** A short, obvious language or framework expression need not be
wrapped merely to make every line look alike.

**Negative example**

```csharp
await ValidateAsync(order);
var json = JsonSerializer.Serialize(order);
request.Content = new StringContent(json, Encoding.UTF8, "application/json");
await client.SendAsync(request);
```

The method jumps from business orchestration into transport encoding details.

**Positive example**

```csharp
await ValidateAsync(order);
await orders.SendAsync(order);
```

The workflow stays at one level; the transport adapter owns serialization.

### SRP — Single Responsibility Principle

**Intent:** Give a module, class, or function one coherent reason to change.

**Review signals:** Look for components combining unrelated policy, persistence, formatting,
orchestration, validation, or external communication.

**Typical violation:** An invoice service calculates totals, writes records, renders a PDF, and
sends email.

**Do not apply mechanically:** Keep behavior that changes together in one cohesive unit. Splitting
every step into a class creates navigation cost and obscures the concept.

**Negative example**

```csharp
class InvoiceService(InvoiceDb db, PdfWriter pdf, EmailClient email)
{
    public async Task CreateAsync(Invoice invoice)
    {
        invoice.Recalculate();
        await db.SaveAsync(invoice);
        var file = pdf.Write(invoice);
        await email.SendAsync(invoice.CustomerEmail, file);
    }
}
```

Calculation, persistence, rendering, and delivery change for different reasons.

**Positive example**

```csharp
class CreateInvoice(InvoiceRepository invoices, InvoiceDelivery delivery)
{
    public async Task ExecuteAsync(Invoice invoice)
    {
        invoice.Recalculate();
        await invoices.SaveAsync(invoice);
        await delivery.SendAsync(invoice);
    }
}
```

The use case coordinates one workflow while focused collaborators own persistence and delivery.

### SoC — Separation of Concerns

**Intent:** Keep distinct concerns behind boundaries that let each evolve without spreading its
details through the others.

**Review signals:** Look for UI code containing persistence rules, domain decisions tied to HTTP
types, cross-cutting policy copied into features, or infrastructure details leaking into core
behavior.

**Typical violation:** A controller queries the database and implements pricing policy.

**Do not apply mechanically:** Boundaries should follow real concerns and change patterns. Extra
layers that only forward calls add ceremony rather than separation.

**Negative example**

```csharp
async Task<IResult> Checkout(HttpRequest request, ShopDb db)
{
    var order = await db.Orders.FindAsync(request.Query["id"]);
    order.Total *= order.Customer.IsVip ? 0.8m : 1m;
    await db.SaveChangesAsync();
    return Results.Ok(order);
}
```

Transport, persistence, and pricing concerns are entangled at the endpoint.

**Positive example**

```csharp
async Task<IResult> Checkout(CheckoutRequest request, CheckoutOrder checkout)
{
    var receipt = await checkout.ExecuteAsync(request.OrderId);
    return Results.Ok(receipt);
}
```

The endpoint translates HTTP input/output while the use case owns application behavior.

### ISP — Interface Segregation Principle

**Intent:** Make clients depend only on the operations they need.

**Review signals:** Look for broad interfaces whose implementations throw, no-op, or receive
irrelevant dependencies; also inspect clients forced to know unrelated capabilities.

**Typical violation:** A read-only report source must implement create, update, and delete.

**Do not apply mechanically:** Do not split a small cohesive contract into one-member interfaces
when its clients use the capabilities together and implementations support the whole contract.

**Negative example**

```csharp
interface IReportStore
{
    Report Load(Guid id);
    void Save(Report report);
    void Delete(Guid id);
}

class ArchiveReportStore : IReportStore
{
    public Report Load(Guid id) => LoadArchive(id);
    public void Save(Report report) => throw new NotSupportedException();
    public void Delete(Guid id) => throw new NotSupportedException();
}
```

The archive is forced to promise unsupported commands.

**Positive example**

```csharp
interface IReportReader { Report Load(Guid id); }
interface IReportWriter { void Save(Report report); }

class ArchiveReportReader : IReportReader
{
    public Report Load(Guid id) => LoadArchive(id);
}
```

Each client and implementation sees only the capability it uses.

### DIP — Dependency Inversion Principle

**Intent:** Keep high-level policy independent of volatile low-level details by placing a stable,
meaningful boundary at the point of variation.

**Review signals:** Look for business behavior constructing network, database, clock, file, or
framework dependencies; ambient service lookup; or abstractions owned by low-level details.

**Typical violation:** Pricing logic creates a concrete SQL repository internally.

**Do not apply mechanically:** A stable local concrete value or pure collaborator may be the
simplest dependency. Do not create an interface for every class or mirror a concrete API without a
real seam.

**Negative example**

```csharp
class RenewalService
{
    public decimal Quote(Guid id)
    {
        var customer = new SqlCustomerRepository().Load(id);
        return customer.IsLoyal ? 80m : 100m;
    }
}
```

Policy is coupled to construction and SQL access.

**Positive example**

```csharp
class RenewalService(ICustomerReader customers)
{
    public decimal Quote(Guid id)
    {
        var customer = customers.Load(id);
        return customer.IsLoyal ? 80m : 100m;
    }
}
```

The policy depends on the capability it needs; composition chooses the SQL adapter.

### LSP — Liskov Substitution Principle

**Intent:** Ensure every subtype or implementation can replace its base abstraction without
breaking accepted inputs, promised results, invariants, or ordinary operations.

**Review signals:** Look for subtype checks in callers, strengthened preconditions, weakened
postconditions, surprising exceptions, ignored methods, or different semantics under one contract.

**Typical violation:** A read-only subclass inherits `Save` and throws for normal use.

**Do not apply mechanically:** Different implementations may vary internally or in documented
nonessential qualities. Inheritance is valid when all subtypes honor the same behavioral contract.

**Negative example**

```csharp
class Document { public virtual void Save() { } }
class ReadOnlyDocument : Document
{
    public override void Save() => throw new NotSupportedException();
}
```

Code accepting `Document` cannot safely use its promised operation.

**Positive example**

```csharp
abstract class Shape { public abstract decimal Area(); }
sealed class Rectangle(decimal width, decimal height) : Shape
{
    public override decimal Area() => width * height;
}
```

The subtype fully honors the base contract and preserves substitutability.

### Principle of Least Astonishment

**Intent:** Make APIs and behavior match reasonable expectations created by names, conventions,
types, and surrounding code.

**Review signals:** Look for queries that mutate state, operations whose names hide I/O, unusual
defaults, inconsistent error behavior, or return values with surprising meanings.

**Typical violation:** `GetBalance()` refreshes remote data and debits an account.

**Do not apply mechanically:** Domain conventions can differ from general conventions. Prefer the
expectations established by the product and repository, and document unavoidable surprises.

**Negative example**

```csharp
decimal GetBalance()
{
    account.ApplyMonthlyFee();
    repository.Save(account);
    return account.Balance;
}
```

A getter-like query performs an unexpected mutation and write.

**Positive example**

```csharp
decimal Balance => account.Balance;

void ApplyMonthlyFee()
{
    account.ApplyMonthlyFee();
    repository.Save(account);
}
```

The query and state-changing command advertise their behavior.

### Information Hiding Principle

**Intent:** Hide design decisions and representations likely to change behind stable,
purpose-oriented interfaces.

**Review signals:** Look for public mutable collections, leaked persistence or transport types,
callers that know storage keys or algorithms, and internals exposed only to enable external
manipulation.

**Typical violation:** An aggregate exposes a mutable list that callers edit directly.

**Do not apply mechanically:** Do not hide information callers legitimately need or add wrappers
that merely rename an already stable public abstraction.

**Negative example**

```csharp
class Order
{
    public List<OrderLine> Lines { get; } = [];
}

order.Lines.Add(new OrderLine(product, quantity));
```

The representation and mutation rules leak to every caller.

**Positive example**

```csharp
class Order
{
    private readonly List<OrderLine> lines = [];
    public IReadOnlyList<OrderLine> Lines => lines;
    public void Add(Product product, int quantity) => lines.Add(new(product, quantity));
}
```

The order controls mutation and can change its representation without changing callers.

### OCP — Open Closed Principle

**Intent:** Let established behavior remain stable while current, recurring variation can be
added through a clear extension seam.

**Review signals:** Look for repeated edits to central conditionals for each new variant, switches
duplicated across modules, or stable policy mixed with variant-specific behavior.

**Typical violation:** Every payment type requires another branch in several checkout methods.

**Do not apply mechanically:** Do not build plug-in systems, hooks, or strategies for hypothetical
variation. A small stable conditional is often clearer; extract a seam when change evidence exists.

**Negative example**

```csharp
decimal Fee(Payment payment) => payment.Kind switch
{
    PaymentKind.Card => payment.Amount * 0.02m,
    PaymentKind.Transfer => 1m,
    _ => 0m
};
```

If payment kinds are actively growing and this switch repeats, each addition modifies established
code in several places.

**Positive example**

```csharp
interface IFeePolicy { decimal Calculate(decimal amount); }

sealed class CardFee : IFeePolicy
{
    public decimal Calculate(decimal amount) => amount * 0.02m;
}
```

When variation is demonstrated, a focused policy lets composition add a kind without editing
other policies.

### Tell, Don't Ask

**Intent:** Ask an object to perform behavior it owns instead of pulling out its state and making
the decision elsewhere.

**Review signals:** Look for callers reading several properties, deciding an object's transition,
then writing state back; repeated external decisions over another object's internals are strongest.

**Typical violation:** A service checks an order status and total before setting its discount.

**Do not apply mechanically:** Purpose-named queries are appropriate for reporting, UI projection,
and decisions that belong to another policy. Avoid moving unrelated orchestration into an entity.

**Negative example**

```csharp
if (order.Status == OrderStatus.Draft && order.Total > 100m)
    order.Discount = 0.1m;
```

The caller owns an order rule and manipulates the result.

**Positive example**

```csharp
order.ApplyVolumeDiscount();
```

The order owns the invariant and exposes the domain operation.

### LoD — Law of Demeter

**Intent:** Limit a component's knowledge to its direct collaborators and avoid coupling it to
their internal object graphs.

**Review signals:** Look for navigation chains, repeated reach-through calls, or code that breaks
when an intermediate object's structure changes.

**Typical violation:** Shipping code traverses order, customer, address, country, and code.

**Do not apply mechanically:** A fluent API, immutable data projection, or simple DTO traversal can
be intentionally transparent. Focus on chains that expose ownership boundaries and changing
internals.

**Negative example**

```csharp
var code = order.Customer.Address.Country.Code;
```

The caller depends on the full internal object graph.

**Positive example**

```csharp
var code = order.DestinationCountryCode;
```

The order exposes the purpose-needed information without leaking the traversal.

### Implementation Reflects Design

**Intent:** Make important architectural boundaries, domain concepts, ownership, and dependency
direction visible in source structure and names.

**Review signals:** Compare stated design with namespaces, projects, dependencies, and code paths;
look for diagrams or docs claiming boundaries that the implementation bypasses.

**Typical violation:** A documented application port exists, but use cases instantiate the SQL
adapter directly.

**Do not apply mechanically:** Do not force every diagram box into a class or preserve obsolete
design documents. Update the design or implementation so the current intent and code agree.

**Negative example**

```csharp
namespace Billing.Application;

class CreateInvoice
{
    private readonly SqlInvoiceRepository invoices = new();
}
```

The source contradicts the claimed application/infrastructure boundary.

**Positive example**

```csharp
namespace Billing.Application
{
    class CreateInvoice(IInvoiceRepository invoices) { }
}

namespace Billing.Infrastructure
{
    class SqlInvoiceRepository : IInvoiceRepository { }
}
```

Names, placement, and dependency direction make the documented boundary visible.

### YAGNI — You Ain’t Gonna Need It

**Intent:** Build for current requirements and demonstrated near-term change, not imagined future
needs.

**Review signals:** Look for unused extension points, configuration with one value, generic
frameworks for one case, uncalled members, or parameters added only for possible future behavior.

**Typical violation:** A one-format exporter introduces plug-in discovery and versioned provider
contracts.

**Do not apply mechanically:** Preserve small low-cost seams when a requirement or established
change pattern makes variation concrete. YAGNI does not justify knowingly irreversible design.

**Negative example**

```csharp
interface IExportPlugin { string Version { get; } byte[] Export(object value); }
class PluginRegistry { /* discovery, priorities, fallback */ }
```

The product currently exports one known report format, so the extension system has no current
consumer.

**Positive example**

```csharp
sealed class CsvReportExporter
{
    public byte[] Export(Report report) => /* current CSV behavior */ [];
}
```

The code directly implements the present requirement and can be refactored when real variation
appears.

## Relationships and Trade-offs

- **SRP — Single Responsibility Principle** asks whether one unit has one coherent reason to
  change; **SoC — Separation of Concerns** asks whether distinct concerns have useful boundaries
  across the design. They overlap without being interchangeable.
- **DRY — Don’t Repeat Yourself** removes duplicated knowledge. **YAGNI — You Ain’t Gonna Need It**
  and **KISS — Keep it simple, stupid** resist extracting an abstraction before the shared concept
  is understood.
- **KISS — Keep it simple, stupid** challenges avoidable indirection in the design used now;
  **YAGNI — You Ain’t Gonna Need It** challenges behavior and extension machinery that no current
  requirement needs. One design can violate both for different reasons.
- **DIP — Dependency Inversion Principle** and **OCP — Open Closed Principle** can reinforce each
  other at a demonstrated variation boundary. YAGNI rejects speculative interfaces and plug-ins.
- **ISP — Interface Segregation Principle** reduces coupling caused by overly broad abstractions;
  it does not require one-member interfaces everywhere.
- **Tell, Don't Ask** and **LoD — Law of Demeter** often reveal the same encapsulation leak from
  different angles: misplaced decisions and excessive object-graph knowledge.
- **Single Level of Abstraction** can reveal a method mixing orchestration with implementation
  details; **IOSP — Integration Operation Segregation Principle** more specifically separates
  project-call composition from logic.
- **FCoI — Favour Composition over Inheritance** is the default reuse heuristic; **LSP — Liskov
  Substitution Principle** identifies inheritance that legitimately models a substitutable
  hierarchy.
- **Information Hiding Principle** protects volatile decisions, while **Principle of Least
  Astonishment** keeps the resulting public behavior predictable.
- **Implementation Reflects Design** checks that intended responsibilities, boundaries, and
  dependency directions remain recognizable in the implementation.
